# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"


# Put here the models you want to manage through the Django Admin
from models import NewTranslation, New
from django.contrib import admin


class NewTranslationInline(admin.StackedInline):
    model = NewTranslation
    extra = 1
    min_num = 1


class NewAdmin(admin.ModelAdmin):
    inlines = [NewTranslationInline]
admin.site.register(New, NewAdmin)

