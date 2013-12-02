# coding: utf-8
from django import template

from app.models import Account, Document, Section
from app import const, forms

register = template.Library()


@register.inclusion_tag('experts_menu.html')
def experts_menu():
    account_counts = Account.objects.filter(user__is_active=True).count()
    
    return {
        'disquss': Document.objects.filter(status=const.STATUS_DISCUSS).count(),
        'accept': Document.objects.filter(status=const.STATUS_ACCEPT).count(),
        'reject': Document.objects.filter(status=const.STATUS_REJECT).count(),
        'account_counts': account_counts
    }


@register.inclusion_tag('filter_form.html')
def filter_form(section):
    return {
        'sections': Section.objects.all(),
        'section': section
    }