#-*- coding:utf-8 -*-
r"""
>>> from django.test.client import Client
>>> from django.contrib.auth.models import User, Group, Permission
>>> from django.core.files import File

>>> from mbco.conference.app.models import *
>>> from mbco.conference.app.const import *
>>> c = Client()

стартовая
=========


регистрация (RU)
================ 
>>> r = c.get('/accounts/register/ru/')
>>> r.status_code
200
>>> r = c.post('/accounts/register/ru/')
>>> r.status_code
200
>>> r = c.post('/accounts/register/ru/', {'email':'user@test.ru', 'password1':'123', 'password2':'123',
...                                     'first_name': 'Иван', 'parent_name': 'Петрович', 'family_name': 'Сидоров',
...                                     'country': 'Россия', 'city': 'Москва','degree':'профессор, кандитат физ.наук',
...                                    'work_place':'Газпром' ,'post':'сотрудник',
...                                    'contact': '8920-233-22-33', 'tos': True
...                                     })

>>> r.status_code
302


активация аккаунта
------------------
>>> from registration.models import RegistrationProfile
>>> rf = RegistrationProfile.objects.all()[0]
>>> r = c.get('/accounts/activate/%s/' % rf.activation_key)

>>> user = User.objects.get(email='user@test.ru')

>>> acc = user.get_profile()
>>> acc.id is None
False

>>> acc.typ == const.RU_TYP
True


регистрация (EN)
================ 
>>> r = c.get('/accounts/register/en/')
>>> r.status_code
200
>>> r = c.post('/accounts/register/en/')
>>> r.status_code
200
>>> r = c.post('/accounts/register/en/', {'email':'userEN@test.ru', 'password1':'123', 'password2':'123',
...                                     'deal':'Dr.','first_name': 'Jhon', 'family_name': 'Gondurasman',
...                                     'country': 'USA', 'city': 'City1','degree':'neznaika',
...                                    'work_place':'GOV' ,'post':'officer',
...                                    'contact': '8920-233-22-221', 'tos': True
...                                     })

>>> r.status_code
302

активация аккаунта
------------------
>>> from registration.models import RegistrationProfile
>>> rf = RegistrationProfile.objects.all().order_by('id')[0]
>>> r = c.get('/accounts/activate/%s/' % rf.activation_key)

>>> user2 = User.objects.get(email='useren@test.ru')

>>> acc2 = user2.get_profile()
>>> acc2.id is None
False

>>> acc2.typ == const.EN_TYP
True


вход на сайт
============
>>> c.login(username=user.username, password='123')
True

просмотр своего профиля 
-----------------------
>>> r = c.get('/account/')
>>> r.status_code
200

добавление тезиса
-----------------
создаём секции
>>> section = Section.objects.create(ru_title=u'Секция 1', en_title=u'Section 1', rank=10)

>>> r = c.get('/account/document/add/')
>>> r.status_code
200

>>> section = getLast(Section)
>>> file1 = open(test_stuff + '1.png')
>>> r = c.post('/account/document/add/', {'title':'document1', 'filename': file1, 'section': section.id})
>>> r.status_code
302

>>> doc = getLast(Document)
>>> doc.status == STATUS_DISCUSS
True

>>> doc.author == acc
True



экспертная часть
----------------
делаем для теста юзера экспертом
>>> user.user_permissions.add(Permission.objects.get(codename='expert'))
>>> user.has_perm('app.expert')
True

просмотр списка тезисов на обсуждении
>>> r = c.get('/documents/disquss/')
>>> r.status_code
200
  

просмотр списка утверждённых тезисов 
>>> r = c.get('/documents/accept/')
>>> r.status_code
200
 

просмотр списка отказанных тезисов 
>>> r = c.get('/documents/reject/')
>>> r.status_code
200

страница обсуждения тезиса
>>> r = c.get('/document/%s/' % doc.id)
>>> r.status_code
200

добавление комментария к тезису (после добавление - редирект на страницу обсуждения)
>>> r = c.post('/document/%s/add_comment/' % doc.id, {'text': 'faq1'})
>>> r.status_code
302

список участников
-----------------
>>> r = c.get('/accounts/list/')
>>> r.status_code
200

сводка по мероприятиям
----------------------
>>> r = c.get('/tours/info/')
>>> r.status_code
200

утверждение или отказ тезиса
-----------------------------
>>> r = c.get('/document/%s/accept/' % doc.id)
>>> r.status_code
200

>>> r = c.post('/document/%s/accept/' % doc.id, {'status_comment':'very good'})
>>> r.status_code
302
>>> doc = Document.objects.get(pk=doc.id)
>>> doc.status == STATUS_ACCEPT
True

>>> r = c.get('/document/%s/reject/' % doc.id)
>>> r.status_code
200

>>> r = c.post('/document/%s/reject/' % doc.id, {'status_comment':'very bad'})
>>> r.status_code
302
>>> doc = Document.objects.get(pk=doc.id)
>>> doc.status == STATUS_REJECT
True


экскурсии
---------
>>> tour = Tour.objects.create(ru_title=u'Экскурсия 1', en_title=u'Tour 1', rank=10)

подача заявки на экскурсию
>>> r = c.get('/tour/%s/toggle/' % tour.id)
>>> r.status_code
302

удаления заявки на экскурсию (по принципу переключателя)
>>> r = c.get('/tour/%s/toggle/' % tour.id)
>>> r.status_code
302



"""
