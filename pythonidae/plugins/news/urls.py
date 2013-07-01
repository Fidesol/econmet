# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.conf.urls.defaults import patterns, include, url

# The URL's shown below will be included in the main urls.py file
# This will be included in the way: /<plugin-name>/<url-definded-here/
urlpatterns = patterns('',

    url(r'^news_list/$', 'plugins.news.views.news_list'),
    url(r'^new/(?P<news_id>.*)/$', 'plugins.news.views.news'),

)
