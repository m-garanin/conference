# coding: utf-8

from django.utils.translation import ugettext_lazy as _


RU_TYP = 10 # русскоязычный аккаунт
EN_TYP = 20 # иноземец


STATUS_DISCUSS = 10
STATUS_ACCEPT = 20
STATUS_REJECT = 30

STATUS_CHOICES = (
    (STATUS_DISCUSS, _(u'Обсуждается')),
    (STATUS_REJECT, _(u'Отклонён')),
    (STATUS_ACCEPT, _(u'Принят'))
)

EN_DEAL_CHOICES = (
    (u'Prof.', u'Prof.'),
    (u'Dr.', u'Dr.'),
    (u'Mr.', u'Mr.'),
    (u'Mrs.', u'Mrs.'),
    (u'Ms.', u'Ms.')
)
