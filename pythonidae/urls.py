# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
import cms_settings
from django.contrib import admin
from subprocess import Popen, PIPE
import os
from plugins_settings import PLUGINS_DIR
import settings

admin.autodiscover()

# Handlers for the 404 and 500 error pages
handler404 = 'cms.views.error_404'
handler500 = 'cms.views.error_500'

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # admin-tools
    url(r'^admin_tools/', include('admin_tools.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')), 

    url(r'^contact/$', 'cms.views.contact'),
    url(r'^partnership/$', 'cms.views.partnership'),
    url(r'^questionary/$', 'cms.views.questionary'),
    url(r'^$', 'cms.views.home', name='home'),
    url(r'^home/$', 'cms.views.home', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': cms_settings.DEFAULT_ACCOUNT_LOGIN}),     #redireccionar a 'login' cuando no este login
    
    # rosetta - Translation module
    url(r'^rosetta/', include('rosetta.urls')),

)

PLUGINS_DIR = os.path.join(settings.PROJECT_ROOT, 'plugins')

# Import the urls files from plugins
directory_list = os.listdir(PLUGINS_DIR)
for plugin in directory_list:
    if os.path.isdir(os.path.join(PLUGINS_DIR, plugin)) and not plugin.startswith('.'):
        try:
            url_path = r'^%s/' % (plugin)
            urlpatterns += patterns('',
                url(url_path, include('plugins.%s.urls' % plugin)),
            )
        except ImportError:
            pass
            # TODO: print a log message

# IMPORTANT: this line must be allways at the end of the patterns
urlpatterns += patterns('',
                url(r'^(?P<path>.*)/$', 'cms.views.page', name='page'),
            )
