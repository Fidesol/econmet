# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from plugins.econmet.models import *
from django.contrib import admin

admin.autodiscover()

handler404 = 'plugins.econmet.views.error_404_view'
handler500 = 'plugins.econmet.views.error_500_view'

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'/admintools/', include('admin_tools.urls')),         
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^$', 'plugins.econmet.views.clinical'),
    url(r'^/?$', 'plugins.econmet.views.clinical'),

    url(r'^login$', 'plugins.econmet.views.mylogin', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/econmet/login','redirect_field_name': 'next'}, name='logout'),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'econmet/home.html'}),     #redireccionar a 'login' cuando no este login

    url(r'^register/(?P<profile>[a-z]+)$', 'plugins.econmet.views.register', name='register'),
    url(r'^register', 'plugins.econmet.views.register', name='register'),
    
    url(r'^clinical/(?P<id>\d+)/(?P<element>[a-z]+)$', 'plugins.econmet.views.thumb_view', name='thumb_view'),
    url(r'^clinical/(?P<id>\d+)$', 'plugins.econmet.views.thumb_view', name='clinical_view_id'),
    url(r'^clinical$', 'plugins.econmet.views.clinical', name='clinical_view'),
    
    url(r'^symptoms$', 'plugins.econmet.views.symptoms', name='symptoms_view'),

    url(r'^analisys/(?P<type>[a-z]+)/(?P<id>\d+)$', 'plugins.econmet.views.analisys', name='analisys_view'),
    url(r'^analisys/(?P<type>[a-z]+)$', 'plugins.econmet.views.analisys', name='analisys_view'),
    url(r'^analisys$', 'plugins.econmet.views.analisys', name='analisys_view'),
    
    url(r'^report/alias/(?P<clinical_id>\d+)$', 'plugins.econmet.views.report_alias', name="report_alias"),
    
    url (r'^diagnose', 'plugins.econmet.views.diagnose', name='diagnose_view'),
    
    url(r'^delete/(?P<clinical_id>\d+)/(?P<model>[a-z]+)/(?P<id>\d+)$', 'plugins.econmet.views.delete', name='delete'),
    
    url(r'^validate/(?P<id>\d+)$', 'plugins.econmet.views.validate', name='validate_view'),
    url(r'^search$', 'plugins.econmet.views.search', name='search_view_id'),
    
    
    url(r'^rosetta/', include('rosetta.urls')),
    
    
)
