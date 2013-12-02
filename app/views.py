# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import check_for_language
from django.views.generic.create_update import update_object, create_object
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.forms import ModelChoiceField, ModelForm, RadioSelect
from django.utils.translation import ugettext_lazy as _

from models import Document, Section, Tour, AccountTour, Account
import forms, const


@login_required
def account(request):
    acc = request.user.get_profile()
    
    def tours():
        acc_tours = list(acc.tours)
        # итератор по экскурсиям. добавляет временный атрибут my_tour
        for t in Tour.objects.all():
            t.title = (acc.typ==const.RU_TYP and t.ru_title) or t.en_title
            t.my_tour = t in acc_tours
            yield t
            
    return direct_to_template(request,
                              template='account/index.html',
                              extra_context={
                                  'account': acc,
                                  'tours': tours,
                                  "documents": Document.objects.filter(author = acc)
                              })


@login_required
def document_add(request):
    acc = request.user.get_profile()

    class SectionModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            if acc.typ == const.RU_TYP:
                return obj.ru_title
            else:
                return obj.en_title

    class DocumentForm(ModelForm):
        section = SectionModelChoiceField(label=_(u'Секция'),
                                          widget=RadioSelect,
                                          queryset=Section.objects.all(),
                                          empty_label=None)
        class Meta:
            model = Document
            fields = ('title', 'filename', 'section', 'desc')

        def save(self):
            obj = super(DocumentForm, self).save(commit=False)
            obj.author = acc
            obj.save()
            obj.to_status(const.STATUS_DISCUSS, acc)
            return obj

    return create_object(request,
                         form_class=DocumentForm,
                         post_save_redirect=reverse('account'),
                         template_name='account/document_form.html')


@login_required
def document_edit(request, document_id):
    acc = request.user.get_profile()

    document = get_object_or_404(Document, pk=document_id, author=acc)
    return update_object(request,
                         form_class=forms.DocumentForm,
                         object_id=document_id,
                         template_name='account/document_form.html',
                         post_save_redirect=reverse('account')
                         )


## экспертная часть
@permission_required('app.expert')
def documents_disquss(request):
    section = request.session.get('section')
    kwargs = {}
    if section and section != '0':
        kwargs['section__id'] = section
    documents = Document.objects.filter(status=const.STATUS_DISCUSS, **kwargs)
    return object_list(request,
                       queryset=documents,
                       template_name='account/documents_disquss.html',
                       extra_context={'section': section})


@permission_required('app.expert')
def documents_accept(request):
    section = request.session.get('section')
    kwargs = {}
    if section and section != '0':
        kwargs['section__id'] = section
    documents = Document.objects.filter(status=const.STATUS_ACCEPT, **kwargs)
    return object_list(request,
                       queryset=documents,
                       template_name='account/documents_accept.html',
                       extra_context={'section': section})


@permission_required('app.expert')
def documents_reject(request):
    section = request.session.get('section')
    kwargs = {}
    if section and section != '0':
        kwargs['section__id'] = section
    documents = Document.objects.filter(status=const.STATUS_REJECT, **kwargs)
    return object_list(request,
                       queryset=documents,
                       template_name='account/documents_reject.html',
                       extra_context={'section': section})


@permission_required('app.expert')
def document_moderate(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return direct_to_template(request,                              
                              extra_context={'document': document,
                                             'author':document.author,
                                             'comments': document.comment_set.all()},
                              template='account/document_moderate.html')


@permission_required('app.expert')
def document_add_comment(request, document_id):
    acc = request.user.get_profile()

    document = get_object_or_404(Document, pk=document_id)

    class Frm(forms.CommentForm):
        def save(self):
            obj = super(Frm, self).save(commit=False)
            obj.author = acc
            obj.document = document
            obj.save()
            add_comment(obj)
            return obj
        
    return create_object(request,
                         form_class=Frm,
                         extra_context={'document':document},
                         post_save_redirect=reverse('document_moderate', args=[document_id]),
                         template_name='account/comment_form.html'
                         )


@permission_required('app.expert')
def document_accept(request, document_id):
    acc = request.user.get_profile()

    document = get_object_or_404(Document, pk=document_id)

    class Frm(forms.DocumentStatusForm):
        def save(self):
            obj = super(Frm, self).save()
            comment = self.cleaned_data['status_comment']
            document.to_status(const.STATUS_ACCEPT, acc, comment)
            change_status(document)
            return obj

    return update_object(request,
                         form_class=Frm,
                         object_id=document_id,
                         extra_context={'document': document},
                         template_name='account/document_accept.html',
                         post_save_redirect=reverse('document_moderate', args=[document_id]))


@permission_required('app.expert')
def document_reject(request, document_id):
    acc = request.user.get_profile()

    document = get_object_or_404(Document, pk=document_id)

    class Frm(forms.DocumentStatusForm):
        def save(self):
            obj = super(Frm, self).save()
            comment = self.cleaned_data['status_comment']
            document.to_status(const.STATUS_REJECT, acc, comment)
            change_status(document)
            return obj

    return update_object(request,
                         form_class=Frm,
                         object_id=document_id,
                         extra_context={'document': document},
                         template_name='account/document_reject.html',
                         post_save_redirect=reverse('document_moderate', args=[document_id]))


@permission_required('app.expert')
def accounts_list(request):
    accounts = Account.objects.filter(user__is_active=True).order_by('id')
    return object_list(request,
                       queryset=accounts,
                       template_name='account/accounts_list.html')


## emeils
def change_status(document):
    # отсылаем автору письмо о смене статуса
    if document.author.typ == const.RU_TYP:
        subject = u'У Ваших тезисов сменился статус'
        lang = 'ru'
    else:
        subject = u'Your thesis\' status was changed'
        lang = 'en'
    message = render_to_string('emails/change_status_%s.txt' % lang, {'document': document})
    send_mail(subject, message, settings.EMAIL_HOST_USER, [document.author.user.email])

    # рассылаем экспертам письмо о смене статуса (всем, кроме инициатора смены статуса)
    subject = u'У тезисов сменился статус'
    domain = Site.objects.get_current().domain
    message = render_to_string('emails/change_status_experts.txt', {
        'document': document,
        'url': 'http://%s%s' % (domain, reverse('document_moderate', args=[document.id]))
    })
    perm = Permission.objects.get(codename='expert')
    send_mail(subject, message, settings.EMAIL_HOST_USER, perm.user_set.filter(is_active=True).\
                                                                exclude(id=document.status_author.user_id).\
                                                                values_list('email', flat=True))
    return


def add_comment(comment):
    u'''при добавление комментария рассылаем письмо всем экспертам, за исключением автора коммента
    '''
    subject = u'У тезисов появился новый комментарий'
    domain = Site.objects.get_current().domain
    message = render_to_string('emails/add_comment.txt', {
        'comment': comment,
        'url': 'http://%s%s' % (domain, reverse('document_moderate', args=[comment.document.id]))
    })
    perm = Permission.objects.get(codename='expert')
    send_mail(subject, message, settings.EMAIL_HOST_USER, perm.user_set.filter(is_active=True).\
                                                                exclude(id=comment.author.user_id).\
                                                                values_list('email', flat=True))
    return


## экскурсии
@login_required
def tour_toggle(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    acc = request.user.get_profile()

    qs = list(AccountTour.objects.filter(tour=tour, account=acc))
    
    if not qs:
        # сперва удаляем все другие туры для данного юзера
        AccountTour.objects.filter(account=acc).delete()
        # создаём тур 
        AccountTour.objects.create(tour=tour, account=acc)
    else:
        qs[0].delete()

    return redirect('account')


@permission_required('app.expert')
def tours_info(request):
    tours = Tour.objects.all()
    return object_list(request,
                       queryset=tours,
                       template_name='account/tours_list.html')


## others
def set_language(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    
    response = HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('lang', None)

        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


def set_filter(request):
    u'устанавливаем фильтр по секциям'
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', '/')
    section = request.POST.get('section', 0)
    request.session['section'] = section
    return redirect(next)
