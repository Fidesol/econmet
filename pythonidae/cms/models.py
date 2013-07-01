# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.db import models
from lib.multiling import MultilingualModel
from django.utils.translation import ugettext_lazy as _

# multilanguage example
# class BookTranslation(models.Model):
#    language = models.ForeignKey("Language")
#    title = models.CharField(max_length=32)
#    description = models.TextField()
#    model = models.ForeignKey("Book")
#        
# class Book(MultilingualModel):
#    ISBN = models.IntegerField()
#       
#    class Meta:
#        translation = BookTranslation
#        multilingual = ['title', 'description']

class Language(models.Model):
    code = models.CharField(max_length=5, verbose_name=_(u'Code'))
    name = models.CharField(max_length=16, verbose_name=_(u'Name'))
    image_active = models.ImageField(upload_to='languages', blank=True, verbose_name=_(u'Image when active'))
    image_inactive = models.ImageField(upload_to='languages', blank=True, verbose_name=_(u'Image when inactive'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

class PageTranslation(models.Model):
    language = models.ForeignKey('Language', verbose_name=_(u'Language'))
    model = models.ForeignKey('Page', verbose_name=_(u'Page'))
    
    # model fields
    title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_(u'Title'))
    # TODO: Aquí hay que ver como insertar imágenes entre el texto, por ejemplo para la página de "personal"
    content = models.TextField(verbose_name=_(u'Contenido'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name=_(u'Translation')


class Page(MultilingualModel):
    """
    Model to store content of 'static' pages.
    Supports multi language.
    """
    alias = models.CharField(max_length=256, verbose_name=_(u'Alias'), help_text=_(u'Field used to identify this page inside the administration list.'))
    url = models.CharField(max_length=256, verbose_name=_(u'URL'), help_text=_(u'Path of the page inside the web, for example: about --> http://example.com/about'))
    image = models.ImageField(upload_to='pages', blank=True, null=True, verbose_name=_(u'Associated image'), help_text=_(u'In some themes, the page can have an image attached, in that case, the image will show in the page (where the designer does).'))
    active = models.BooleanField(default=True, verbose_name=_(u'Active page'), help_text=_('If false, the page will not be shown.'))
    
    def __unicode__(self):
        return self.alias
        
    class Meta:
        translation = PageTranslation
        multilingual = ['title', 'content']
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Pages')

class MenuTranslation(models.Model):
    language = models.ForeignKey('Language', verbose_name=_(u'Language'))
    model = models.ForeignKey('Menu')
    
    name = models.CharField(max_length=100, verbose_name=_(u'Name'))
    
    def __unicode__(self):
        return self.name
    
class Menu(MultilingualModel):
    """
    Model to store the menu bar.
    Supports multi language.
    """
    alias = models.CharField(max_length=256, verbose_name=_(u'Alias'), help_text=_(u'Field used to identify the menu in the list.'))
    nav_option = models.CharField(max_length=100, primary_key=True, verbose_name=_(u'Nav option'), help_text=_(u'Field used in the theme to identify active menu option.'))
    page = models.ForeignKey('Page', verbose_name=_(u'Page'), help_text=_(u'Page that will be shown.'))
    show_owner_page = models.BooleanField(verbose_name=_(u'Show page'), help_text=_(u'If this option is marked, the page selected before will be shown, if not, the firts page in the submenu will be shown.'))
    parent_menu = models.ForeignKey('Menu', null = True, blank = True, verbose_name=_(u'Parent menu'), help_text=_(u'If this menu will be a submenu of another.'))
    
    def __unicode__(self):
        return self.alias
        
    class Meta:
        translation = MenuTranslation
        multilingual = ['name']
        verbose_name = _(u'Menu')
        verbose_name_plural = _(u'Menus')

class FixedValueTranslation(models.Model):
    language = models.ForeignKey('Language', verbose_name=_(u'Language'))
    model = models.ForeignKey('FixedValue')
    
    value = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.value
    
class FixedValue(MultilingualModel):
    """
    Model to store fixed values in the web.
    Supports multi language.

    """

    group = models.CharField(max_length=256, verbose_name=_(u'Group'))
    key = models.CharField(max_length=256, verbose_name=_(u'Key'))
    
    def __unicode__(self):
        return self.group + '.' + self.key
    
    class Meta:
        translation = FixedValueTranslation
        multilingual = ['value']
        verbose_name = _('Fixed Value')
        verbose_name_plural = _('Fixed Values')
        
class Configuration(models.Model):
    """
    Model to store configuration values.
    """
    group = models.CharField(max_length=256, verbose_name=_(u'Group'))
    key = models.CharField(max_length=256, verbose_name=_(u'Key'))
    value = models.CharField(max_length=500, verbose_name=_(u'Value'))
    data_type = models.CharField(max_length=15, verbose_name=_(u'Data type')) # bool, text, number, etc.
    label = models.CharField(max_length=256, verbose_name=_(u'Label'))
    help_text = models.CharField(max_length=256, blank=True, verbose_name=_(u'Help text'))

    def __unicode__(self):
        return self.group + '.' + self.key

    class Meta:
        verbose_name = _(u'Configuration')
        verbose_name_plural = _(u'Configurations')
 

# TODO: translate the questionary models.

class QuestionaryTranslation(models.Model):
    language = models.ForeignKey('Language')
    model = models.ForeignKey('Questionary')
    
    name = models.CharField(max_length=256)
    text = models.TextField()
        
    def __unicode__(self):
        return self.name

class Questionary(MultilingualModel):
    """
    Model to store questionaries.
    Supports multi language
    """
    alias = models.CharField(max_length=256)
    alias.help_text = _(u'Campo utilizado para distinguir el cuestionario dentro del listado de administración')
    questions = models.ManyToManyField('Question')
    parameters = models.ManyToManyField('Parameter')
    
    def __unicode__(self):
        return self.alias
    
    class Meta:
        translation = QuestionaryTranslation
        multilingual = ['name', 'text']
        verbose_name = _(u'Questionary')
        verbose_name_plural = _(u'Questionaries')
       
class QuestionTranslation(models.Model):
    language = models.ForeignKey('Language')
    model = models.ForeignKey('Question')
    
    #models fields
    question = models.TextField()
    
    def __unicode__(self):
        return self.question
    
    
class Question(MultilingualModel):
    """
    Model to store questions for the questionary.
    Supports multi language.
    """
    response_text = models.BooleanField() # if true, the form will show a textbox for user's input
    just_one_response = models.BooleanField() # if true, the form will show option buttons, not check boxes.
    complex_question = models.ManyToManyField('Question', blank = True, null = True) #if a question is composed by other questions.
    responses = models.ManyToManyField('Response', blank = True, null = True)
    #response = models.ForeignKey('Response', blank=True, null=True)
    alias = models.CharField(max_length=256)
    alias.help_text = _(u'Campo utilizado para distinguir la pregunta dentro del listado de administración')
    is_required = models.BooleanField()

    def __unicode__(self):
        return self.alias

    class Meta:
        translation = QuestionTranslation
        multilingual = ['question']
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')

class ParameterTranslation(models.Model):
    language = models.ForeignKey('Language')
    model = models.ForeignKey('Parameter')
    
    parameter = models.TextField()
    unit = models.TextField()
    
    def __unicode__(self):
        return self.parameter
    
class Parameter(MultilingualModel):
    """
    Model to store parameters fro the questionary.
    Supports multi language.
    """
    alias = models.CharField(max_length=256)
    alias.help_text = _(u'Campo utilizado para distinguir el parametro dentro del listado de administración')
    is_required = models.BooleanField()
    
    def __unicode__(self):
        return self.alias
    
    class Meta:
        translation = ParameterTranslation
        multilingual = ['parameter', 'unit']
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')

class ResponseTranslation(models.Model):
    language = models.ForeignKey('Language')
    model = models.ForeignKey('Response')
    
    response = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.response
     
class Response(MultilingualModel):
    """
    Model to store question's responses.
    Supports multi language.
    """
    alias = models.CharField(max_length=256)
    alias.help_text = _(u'Campo utilizado para distinguir la respuesta dentro del listado de administración')

    def __unicode__(self):
        return self.alias    
    
    class Meta:
        translation = ResponseTranslation
        multilingual = ['response']
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
        
