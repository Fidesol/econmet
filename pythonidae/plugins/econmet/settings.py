# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.utils.translation import ugettext_lazy as _

# Put in this tuple the models you want to show in the Django admin
# for more information about this variable go to the official 
# django-fluent-dashboard module: https://github.com/edoburu/django-fluent-dashboard
ECONMET_FLUENT_DASHBOARD_APP_GROUPS = (_('Econmet Plug-in'), {
                                            'models': (
                                            'plugins.econmet.models.Clinical',
                                            'plugins.econmet.models.Illness',
                                            'plugins.econmet.models.Report',
                                            'plugins.econmet.models.AnalisysParameter',
                                            'plugins.econmet.models.SymptomsParameter',
                                            'plugins.econmet.models.ParameterValues',
                                            'plugins.econmet.models.MedicalProfile',
                                            'plugins.econmet.models.LaboratoryProfile',
                                            ),
                                    'module': 'CmsAppIconList',
                                    'collapsible': False,
                                    })

# If the PLUGIN_FLUENT_DASHBOARD_APP_GROUPS is defined before, and
# module is defined as 'CmsAppIconList', you must define the images
# that will be shown for each model.
ECONMET_FLUENT_DASHBOARD_APP_ICONS = {
    'econmet/clinical': 'themes/econmet/images/admin/clinical.png',
    'econmet/illness': 'themes/econmet/images/admin/illness.png',
    'econmet/analisysparameter': 'themes/econmet/images/admin/analisys.png',
    'econmet/symptomsparameter': 'themes/econmet/images/admin/symptoms.png',
    'econmet/report': 'themes/econmet/images/admin/report.png',
    'econmet/medicalprofile': 'themes/econmet/images/admin/medical.png',
    'econmet/laboratoryprofile': 'themes/econmet/images/admin/laboratory.png',
    'econmet/parametervalues': 'themes/econmet/images/admin/parameters.png',
}

# Must the plugin have a menu entry in the main menu?
ECONMET_HAS_MENU = True

# If PLUGIN_HAS_MENU is defined to True, define the menu's title
ECONMET_MENU_TITLE = _('Econmet')

# If PLUGIN_HAS_MENU is defined to True, define the root url of your plugin
ECONMET_MENU_URL = '/econmet/clinical.html'

# Add the locale directory as preference than pythonaide locale path
LOCALE_PATH = '/econmet/locale'
