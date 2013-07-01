# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.contrib import admin
from cms.models import *

class PageTranslationInline(admin.StackedInline):
    model = PageTranslation
    extra = 1
    min_num = 1

class PageAdmin(admin.ModelAdmin):
    list_display = ('alias', 'url', 'active')
    inlines = [PageTranslationInline]
admin.site.register(Page, PageAdmin)

class MenuTranslationInline(admin.StackedInline):
    model = MenuTranslation
    extra = 1
    min_num = 1
    
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuTranslationInline]
admin.site.register(Menu, MenuAdmin)

class FixedValueTranslationInline(admin.StackedInline):
    model = FixedValueTranslation
    extra = 1
    min_num = 1
    
class FixedValueAdmin(admin.ModelAdmin):
    inlines = [FixedValueTranslationInline]
admin.site.register(FixedValue, FixedValueAdmin)

class LanguageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Language, LanguageAdmin)

class ConfigurationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Configuration, ConfigurationAdmin)

# TODO: Models below must be moved to a plug-in


class QuestionaryTranslationInline(admin.StackedInline):
    model = QuestionaryTranslation
    extra = 1
    min_num = 1
    
class QuestionaryAdmin(admin.ModelAdmin):
    inlines = [QuestionaryTranslationInline]
#admin.site.register(Questionary, QuestionaryAdmin)

class QuestionTranslationInline(admin.StackedInline):
    model = QuestionTranslation
    extra = 1
    min_num = 1
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionTranslationInline]
#admin.site.register(Question, QuestionAdmin)

class ResponseTranslationInline(admin.StackedInline):
    model = ResponseTranslation
    extra = 1
    min_num = 1
    
class ResponseAdmin(admin.ModelAdmin):
    inlines = [ResponseTranslationInline]
#admin.site.register(Response, ResponseAdmin)

class ParameterTranslationInline(admin.StackedInline):
    model = ParameterTranslation
    extra = 1
    min_num = 1
    
class ParameterAdmin(admin.ModelAdmin):
    inlines = [ParameterTranslationInline]
#admin.site.register(Parameter, ParameterAdmin)

# Example for multilingual objects
# class BookTranslationInline(admin.StackedInline):
#    model = BookTranslation
#    extra = 1
#    min_num = 1
#
#class BookAdmin(admin.ModelAdmin):
#    list_display = ["ISBN"]
#    inlines = [BookTranslationInline]
#
#admin.site.register(Book, BookAdmin)
