# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.utils.translation import ugettext_lazy as _

# Put in this tuple the models you want to show in the Django admin
# for more information about this variable go to the official 
# django-fluent-dashboard module: https://github.com/edoburu/django-fluent-dashboard
NEWS_FLUENT_DASHBOARD_APP_GROUPS = (_('Products Plug-in'), {
                                            'models': (
                                            'plugins.news.models.Product',
                                            ),
                                    'module': 'CmsAppIconList',
                                    'collapsible': False,
                                    })

# If the NEWS_FLUENT_DASHBOARD_APP_GROUPS is defined before, and
# module is defined as 'CmsAppIconList', you must define the images
# that will be shown for each model.
NEWS_FLUENT_DASHBOARD_APP_ICONS = {
    'products/product': 'images/admin/admin_products.png',
}

# Must the plugin have a menu entry in the main menu?
NEWS_HAS_MENU = True

# If NEWS_HAS_MENU is defined to True, define the menu's title
NEWS_MENU_TITLE = _('Products')

# If NEWS_HAS_MENU is defined to True, define the root url of your plugin
NEWS_MENU_URL = '/products'
