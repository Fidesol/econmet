# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.db import models
from django.utils.translation import ugettext_lazy as _
from lib.multiling import MultilingualModel
from cms.models import Language


# TODO: Models below must be extracted to a plug-in
class ProductTranslation(models.Model):
    language = models.ForeignKey(Language, verbose_name=_(u'Language'))
    model = models.ForeignKey('Product')

    #model fields
    name = models.CharField(max_length=256, verbose_name=_(u'Name'))
    description = models.TextField(verbose_name=_(u'Description'))

    def __unicode__(self):
        return self.name


class Product(MultilingualModel):
    """
    Model to store products.
    Supports multi language.
    """
    alias = models.CharField(max_length=256, help_text=_(u'Field used to identify the product in the administration list.'))
    productImage = models.ManyToManyField('ProductImage', verbose_name=_(u'Products images'))

    def __unicode__(self):
        return self.alias

    class Meta:
        translation = ProductTranslation
        multilingual = ['name', 'description']
        verbose_name = _(u'Product')
        verbose_name_plural = _(u'Products')

    #def __unicode__(self):
    #    return self.name_es


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, verbose_name=_(u'Image'))

    def __unicode__(self):
        return self.image.name

    class Meta:
        verbose_name = _(u'Product Image')
        verbose_name_plural = _(u'Product Images')


