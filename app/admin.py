# coding: utf-8
from django.contrib import admin

from models import *


admin.site.register(Account)
admin.site.register(Document)
admin.site.register(StatusLog)
admin.site.register(Comment)
admin.site.register(Section)
admin.site.register(Tour)