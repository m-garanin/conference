#-*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

from registration.views import register

import views, forms


urlpatterns = patterns('',
    url(r'^register/ru/$', register,
        {'form_class': forms.RURegForm},
        name='registration_register_ru'),

    url(r'^register/en/$', register,
        {'form_class': forms.ENRegForm},
        name='registration_register_en'),
                       
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'},
        name='auth_logout'),

    (r'^', include('registration.urls')),
)
