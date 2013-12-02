# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from registration.models import RegistrationProfile

from models import Account, Document, Comment
import const


latin = r'^[a-zA-Z0-9]+$'
datetime_input_format = '%d.%m.%Y %H:%M'

class RURegForm(forms.Form):
    u""" форма регистрации русскоязычного аккаунта. требуем уникальности логина
    """

    email = forms.EmailField(label=u'Email',
                             widget=forms.TextInput(attrs={'class':'text'})
                             )
     
    password1 = forms.RegexField(label=u'Пароль',
                                regex=latin,
                                max_length=20,
                                help_text='допустимы латиница и цифры',
                                widget=forms.PasswordInput(attrs={'class':'text'}))

    password2 = forms.RegexField(label=u'Пароль(повтор)',
                                 regex=latin,
                                 max_length=20,
                                 widget=forms.PasswordInput(attrs={'class':'text'}))

    family_name = forms.CharField(label=u'Фамилия')
    first_name = forms.CharField(label=u'Имя')
    parent_name = forms.CharField(label=u'Отчество')

    country = forms.CharField(label=u'Страна')
    city = forms.CharField(label=u'Город')

    degree = forms.CharField(label=u'Учёная степень и звание', required=False)
    work_place = forms.CharField(label=u'Организация', required=False)
    post = forms.CharField(label=u'Должность', required=False)

    contact = forms.CharField(label=u'Моб.телефон')

    tos = forms.BooleanField(label=u'Согласен на публикацию своих данных в целях конференции') 

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.

        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.

        """
        args = self.cleaned_data.copy()
        args.pop('email')
        args.pop('password1')
        args.pop('password2')
        args.pop('tos')

        args['typ'] = const.RU_TYP
        
        acc = Account.objects.create(**args)

        new_user = RegistrationProfile.objects.create_inactive_user(username=str(acc.id),
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'].lower(),
                                                                    profile_callback=profile_callback)
        acc.user = new_user
        acc.save()

        return new_user


class ENRegForm(forms.Form):
    u""" форма регистрации английского аккаунта. требуем уникальности логина
    """

    email = forms.EmailField(label=u'Email',
                             widget=forms.TextInput(attrs={'class':'text'})
                             )
    
    password1 = forms.RegexField(label=u'Password',
                                regex=latin,
                                max_length=20,
                                help_text='Latin characters and numerals',
                                widget=forms.PasswordInput(attrs={'class':'text'}))

    password2 = forms.RegexField(label=u'Password(repeat)',
                                 regex=latin,
                                 max_length=20,
                                 widget=forms.PasswordInput(attrs={'class':'text'}))
    
    deal = forms.ChoiceField(label=u'Title', choices=const.EN_DEAL_CHOICES)
    first_name = forms.CharField(label=u'First name')
    family_name = forms.CharField(label=u'Family name')

    country = forms.CharField(label=u'Country')
    city = forms.CharField(label=u'City')

    degree = forms.CharField(label=u'IRA affiliation', required=False)
    work_place = forms.CharField(label=u'Place of work', required=False)
    post = forms.CharField(label=u'Position', required=False)

    contact = forms.CharField(label=u'Mobile phone')

    tos = forms.BooleanField(label=u'I give my consent to the publishing of my personal data.') 

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data


    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.

        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.

        """
        args = self.cleaned_data.copy()
        args.pop('email')
        args.pop('password1')
        args.pop('password2')
        args.pop('tos')
        args['typ'] = const.EN_TYP
        
        acc = Account.objects.create(**args)
        
        new_user = RegistrationProfile.objects.create_inactive_user(username=str(acc.id),
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'].lower(),
                                                                    profile_callback=profile_callback)
        acc.user = new_user
        acc.save()

        return new_user





class DocumentForm(forms.ModelForm):
    #section = forms.ChoiceField(label=(u'Секция'), widget=forms.RadioSelect)
    class Meta:
        model = Document
        fields = ('title', 'filename', 'section', 'desc')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class DocumentStatusForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('status_comment',)
