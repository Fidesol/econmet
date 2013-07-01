# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.conf.urls.defaults import patterns, url

# The URL's shown below will be included in the main urls.py file
# This will be included in the way: /<plugin-name>/<url-definded-here/
urlpatterns = patterns('',

    url(r'^$', 'plugins.products.views.product_list'),
    url(r'^/(?P<product_id>.*)/$', 'plugins.products.views.product'),

)
