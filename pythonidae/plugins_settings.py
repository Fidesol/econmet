# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.utils.translation import ugettext_lazy as _
from subprocess import Popen, PIPE
import settings
import os

PLUGINS_DIR = os.path.join(settings.PROJECT_ROOT, 'plugins')
PLUGINS_MENUS = {}

# Import the configuration settings files for each plug-in
directory_list = os.listdir(PLUGINS_DIR)
for plugin in directory_list:
    if os.path.isdir(os.path.join(PLUGINS_DIR, plugin)) and not plugin.startswith('.'):
        try:
            config_module = __import__('plugins.%s.settings' % plugin, globals(), locals(), 'fidesolCMS')
            # Load the config settings properties into the local scope.
            for setting in dir(config_module):
                if setting == setting.upper():
                    locals()[setting] = getattr(config_module, setting)

                    # There are some relevant configurations, that in the case they exists, must be added
                    # to general configurations.

                    # gets the fluent dashboard configurations
                    if setting.endswith('_FLUENT_DASHBOARD_APP_GROUPS'):
                        settings.FLUENT_DASHBOARD_APP_GROUPS = settings.FLUENT_DASHBOARD_APP_GROUPS + (getattr(config_module, setting),)
                    if setting.endswith('_FLUENT_DASHBOARD_APP_ICONS'):
                        temp_dict = getattr(config_module, setting)
                        for key, value in temp_dict.items():
                            settings.FLUENT_DASHBOARD_APP_ICONS[key] = value

                    # Get configurations relative to menu's
                    if setting.endswith('_HAS_MENU'):
                        PLUGINS_MENUS[plugin] = {}
                    if setting.endswith('_MENU_TITLE'): 
                        PLUGINS_MENUS[plugin]['title'] = getattr(config_module, setting)
                    if setting.endswith('_MENU_URL'):
                        PLUGINS_MENUS[plugin]['url'] = getattr(config_module, setting)

        except ImportError:
            pass
            # TODO: print a log message

        # Add the plugin to INSTALLED_APPS
        app = 'plugins.%s' % plugin
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + (app,)
    
        # Add the locale to LOCALE_PATHS
        try:
            locale = settings.PROJECT_ROOT + '/plugins'+ getattr(config_module, 'LOCALE_PATH')
            settings.LOCALE_PATHS = (locale,) + settings.LOCALE_PATHS
        except AttributeError:
            pass
