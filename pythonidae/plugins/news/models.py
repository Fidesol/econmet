# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from cms.models import Language
from django.db import models
from django.utils.translation import ugettext_lazy as _
from lib.multiling import MultilingualModel

class NewTranslation(models.Model):
    language = models.ForeignKey(Language, verbose_name=_('Language'))
    model = models.ForeignKey('New')
    
    #models fields
    title = models.CharField(max_length=256)
    content = models.TextField()
    
    def __unicode__(self):
        return self.title

class New(MultilingualModel):
    """
    Model to store news.
    Supports multi language.

    """
    alias = models.CharField(max_length=256, help_text=_(u'Field used to identify the new in the administration list.'))
    
    def __unicode__(self):
        return self.alias

    class Meta:
        translation = NewTranslation
        multilingual = ['title', 'content']
        verbose_name = _(u'New')
        verbose_name_plural = _(u'News')

