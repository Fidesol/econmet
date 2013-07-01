# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

# Create your views here.
from django.shortcuts import render, get_object_or_404
from cms.models import Language, Menu
from plugins.products.models import Product


def product_list(request):
    products = list(Product.objects.all())

    template_name = 'product_list.html'

    return render(request, template_name, {
        'products': products,
        'menu': list(Menu.objects.filter(parent_menu=None)),
        'submenu': None,
        'language': list(Language.objects.all()),
    })


def product(request, product_id):
    MAX_WIDTH_IMG = 350
    MAX_HEIGHT_IMG = 350
    MAX_WIDTH_CONTENT = 965

    product = get_object_or_404(Product, pk=product_id)
    images = list(product.productImage.all())

    if images:
        img_width = images[0].image.width + 30
        img_height = images[0].image.height
        if img_width > MAX_WIDTH_IMG:
            img_width = MAX_WIDTH_IMG
            img_height = MAX_HEIGHT_IMG
        data_width = MAX_WIDTH_CONTENT - img_width - 20
    else:
        images = None
        img_width = None
        data_width = None
        img_height = None

    template_name = 'product.html'
    return render(request, template_name, {
        'img': images,
        'img_width': img_width,
        'img_height': img_height,
        'data_width': data_width,
        'product': product,
        'menu': list(Menu.objects.filter(parent_menu=None)),
        'submenu': None,
        'language': list(Language.objects.all()),
    })
