# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

# Put here the models you want to manage through the Django Admin
from models import ProductTranslation, Product, ProductImage
from django.contrib import admin


class ProductTranslationInline(admin.StackedInline):
    model = ProductTranslation
    extra = 1
    min_num = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductTranslationInline]
admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProductImage, ProductImageAdmin)

