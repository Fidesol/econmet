# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from cms.models import Configuration
import settings
import os

# Settings for the CMS app

try:
    theme_selected = Configuration.objects.filter(group='theme', key='selected')[0].value
except:
    theme_selected = 'default'

DEFAULT_THEME = 'default'
DEFAULT_BASE_TEMPLATE = 'base.html'
THEMES_DIR = 'themes'
THEME_STATIC_URL = 'static'
DEFAULT_ACCOUNT_LOGIN = theme_selected + '/home.html'

THEME_STATIC_ROOT = os.path.join(settings.PROJECT_ROOT, THEMES_DIR, theme_selected, THEME_STATIC_URL) + '/'
