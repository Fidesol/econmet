# -*- coding: utf-8 -*-
from cms.models import Configuration, FixedValue
from settings import STATIC_URL, plugins_settings
from cms_settings import DEFAULT_THEME, DEFAULT_BASE_TEMPLATE, THEMES_DIR, THEME_STATIC_URL
import os

def config_data(request):
    """
    Makes accesible in the templates the config_data variable
    that stores the configurations in the Configuration model.

    """

    configs = Configuration.objects.all()
    dict = {'config_data': {}}

    groups = Configuration.objects.all().values('group').distinct()
    for g in groups:
	dict['config_data'][g['group']] = {}

    for c in configs:
	dict['config_data'][c.group][c.key] = c.value

    return dict

def fixed_values(request):
    """
    Makes accesible in the templates the fixed_value variable
    that stores the values in the FixedValue model.

    """

    fixed_values = FixedValue.objects.all()
    dict = {'fixed_values': {}}

    groups = FixedValue.objects.all().values('group').distinct()
    for g in groups:
    	dict['fixed_values'][g['group']] = {}

    for c in fixed_values:
	dict['fixed_values'][c.group][c.key] = c.value

    return dict	

def theme_info(request):
    """
    Makes accesible in the templates some constants useful for themes.

    """
    
    try:
        theme_selected = Configuration.objects.filter(group='theme', key='selected')[0]
        theme_name = theme_selected.value
    except:
        theme_name = DEFAULT_THEME
    
    return {'BASE_TEMPLATE': os.path.join(theme_name,  DEFAULT_BASE_TEMPLATE), 'THEME_STATIC_URL': os.path.join(STATIC_URL, 'themes', theme_name) + '/'}

def plugins_menus(request):
    """
    Makes accesible in the templates the PLUGINS_MENUS variable that
    stores the menu elements for the plug-ins.
    
    """

    return {'PLUGINS_MENUS': plugins_settings.PLUGINS_MENUS} 

def lang(request):
    """
    Makes accesible in the templates LANG constant that contains
    the language of the request.
    
    """

    # Gets the language to pass to the template
    try:
        lang = request.COOKIES['language']
    except:
        lang = request.META['HTTP_ACCEPT_LANGUAGE'].split('-')[0]        

    return {'LANG': lang}

