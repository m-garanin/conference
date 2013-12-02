from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('app.views',
    url(r'^account/$', 'account', name='account'),
    url(r'^account/document/add/$', 'document_add', name='document_add'),
    #url(r'^account/document/(\d+)/edit/$', 'document_edit', name='document_edit'),
    url(r'^accounts/list/$', 'accounts_list', name='accounts_list'),

    url(r'^document/(\d+)/$', 'document_moderate', name='document_moderate'),
    url(r'^documents/disquss/$', 'documents_disquss', name='documents_disquss'),
    url(r'^documents/accept/$', 'documents_accept', name='documents_accept'),
    url(r'^documents/reject/$', 'documents_reject', name='documents_reject'),
    url(r'^document/(\d+)/add_comment/$', 'document_add_comment', name='document_add_comment'),
    url(r'^document/(\d+)/accept/$', 'document_accept', name='document_accept'),
    url(r'^document/(\d+)/reject/$', 'document_reject', name='document_reject'),

    url(r'^tour/(\d+)/toggle/$', 'tour_toggle', name='tour_toggle'),
    url(r'^tours/info/$', 'tours_info', name='tours_info'),

    url(r'^setlang/', 'set_language', name='set_language'),
    url(r'^setfilter/', 'set_filter', name='set_filter'),
)

urlpatterns += patterns('',
    (r'^accounts/', include('app.urls_accounts')), # registration
)
  
