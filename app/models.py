# coding: utf-8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import const, utils


class Account(models.Model):
    u"учётная запись"
    user = models.ForeignKey(User, unique=True, null=True)

    typ = models.IntegerField()
    
    deal = models.CharField(_(u'Обращение'), max_length=10, blank=True) 

    first_name = models.CharField(_(u'Имя'), max_length=50)
    parent_name = models.CharField(_(u'Отчество'), max_length=50, blank=True)
    family_name = models.CharField(_(u'Фамилия'), max_length=50)
    
    country = models.CharField(_(u'Страна'), max_length=100)
    city = models.CharField(_(u'Город'), max_length=100)

    degree = models.CharField(_(u'Учёная степень и звание'), max_length=255, blank=True)
    work_place = models.CharField(_(u'Место работы'), max_length=255, blank=True)
    post = models.CharField(_(u'Должность'), max_length=255, blank=True)

    contact = models.CharField(_(u'Моб.телефоны'), max_length=255, blank=True)

    @property
    def title(self):
        if self.typ == const.RU_TYP:
            return u'%s %s %s' % (self.family_name, self.first_name, self.parent_name)
        else:
            return u'%s %s %s' % (self.deal, self.family_name, self.first_name)

    @property
    def tours(self):
        u"QS по экскурсиям в которые записан аккаунт"
        return Tour.objects.filter(accounttour__account=self)
    
                
    def __unicode__(self):
        return u"%d" % self.id

    class Meta:
        permissions = (
            ("expert", u"эксперт"),
            ("superexpert", u"супер-эксперт")
        )


class Document(models.Model):
    u"модель тезиса"
    author = models.ForeignKey(Account)
    title = models.CharField(_(u'Наименование тезисов'), max_length=255)
    filename = models.FileField(_(u'Файл'), upload_to=lambda x,y: utils.upload_to_docs(x, y))
    desc = models.TextField(_(u'Описание'), blank=True)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    section = models.ForeignKey('Section', verbose_name=_(u'Секция'))

    status = models.PositiveSmallIntegerField(_(u'Статус документа'),
                                              choices=const.STATUS_CHOICES,
                                              null=True)
    status_date = models.DateTimeField(_(u'Время смены статуса'), null=True)
    status_comment = models.TextField(_(u'Комментарий к статусу'), blank=True)
    status_author = models.ForeignKey(Account, verbose_name=_(u'Автор статуса'),
                                      null=True, related_name='status_author')

    def get_filename(self):
        return str(self.filename).split('/')[-1]

    def to_status(self, status, author, comment=''):
        u"метод для смены статуса и логирование прежнего статуса"
        if self.status:
            StatusLog.objects.create(
                document=self,
                status=self.status,
                status_date=self.status_date,
                status_comment=self.status_comment,
                status_author=self.status_author
            )
        self.status = status
        self.status_comment = comment
        self.status_author = author
        self.status_date = datetime.now()
        self.save()
        return

    def __unicode__(self):
        return self.title


class StatusLog(models.Model):
    u"лог смены статуса"
    document = models.ForeignKey(Document)
    status = models.PositiveSmallIntegerField(_(u'Статус документа'),
                                              choices=const.STATUS_CHOICES)
    status_date = models.DateTimeField(_(u'Время смены статуса'))
    status_comment = models.TextField(_(u'Комментарий к статусу'))
    status_author = models.ForeignKey(Account, verbose_name=_(u'Автор статуса'))

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ['-status_date']


class Comment(models.Model):
    u"комментарий к тезису"
    author = models.ForeignKey(Account)
    document = models.ForeignKey(Document)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    text = models.TextField(_(u'Текст комментария'))


    def __unicode__(self):
        return u'Комментарий к %s' % self.document

    class Meta:
        ordering = ['-date_create']


class Section(models.Model):
    u"справочник секция"
    ru_title = models.TextField(_(u'Название (русское)') )
    en_title = models.TextField(_(u'Название (английское)') )
    rank = models.PositiveIntegerField(_(u'Приоритет'), default=10)

    def __unicode__(self):
        return self.ru_title

    class Meta:
        ordering = ['-rank', 'ru_title']


class Tour(models.Model):
    u"экскурсии"
    ru_title = models.TextField(_(u'Название (русское)') )
    en_title = models.TextField(_(u'Название (английское)') )
    rank = models.PositiveIntegerField(_(u'Приоритет'), default=10)

    @property
    def accounts(self):
        return Account.objects.filter(accounttour__tour=self)

    def __unicode__(self):
        return self.ru_title

    class Meta:
        ordering = ['-rank', 'ru_title']


class AccountTour(models.Model):
    u"заявки на экскурсии"
    account = models.ForeignKey(Account)
    tour = models.ForeignKey(Tour)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return u'%s %s' % (self.account, self.tour)

    class Meta:
        unique_together = (('account', 'tour'),)
