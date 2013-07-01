# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.shortcuts import render, get_object_or_404
from cms.models import Language, Configuration, Page, Menu
from models import New
from django.utils.translation import ugettext_lazy as _


def _smart_truncate(content, length=100, suffix='...'):
    """
    Truncates a string to 'length' characters.

    """

    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def news_list(request):
    """
    Shows the list of news

    """

    MAX_WIDTH_IMG = 350
    MAX_HEIGHT_IMG = 350
    MAX_WIDTH_CONTENT = 950

    try:
        # FIXME: fix this, page??
        img_width = page.image.width + 30
        img_height = page.image.height
        if img_width > MAX_WIDTH_IMG:
            img_width = MAX_WIDTH_IMG
            img_height = MAX_HEIGHT_IMG
        data_width = MAX_WIDTH_CONTENT - img_width - 20
    except:
        img_width = None
        data_width = None
        img_height = None

    news_array = []
    for new in list(New.objects.all()):
        content = new.content
        news_array.append({'id': new.id, 'title': new.title, 'content': content})

    return render(request, 'news_list.html', {
        'img_width': img_width,
        'img_height': img_height,
        'data_width': data_width,
        'news': news_array,
        'menu': list(Menu.objects.filter(parent_menu=None)),
        'submenu': None,
        'language': list(Language.objects.all()),
    })


def news(request, news_id):
    """
    Shows a new

    """

    new = New.objects.get(id=news_id)

    return render(request, 'new.html', {
        'new': new,
        'menu': list(Menu.objects.filter(parent_menu=None)),
        'submenu': None,
        'language': list(Language.objects.all()),
    })
