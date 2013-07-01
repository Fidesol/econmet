# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import logout
from cms.models import Language
from lib.multiling import MultilingualModel


class Clinical(models.Model):
    """ Models a clinical case """
    history_number = models.CharField(max_length=255, verbose_name=_('History Number'))
    illness = models.ManyToManyField('Illness', blank=True, null=True, verbose_name = _('Illness'))
    analisys = models.ManyToManyField('Analisys', blank=True, null=True, verbose_name= _('Analisys'))
    symptoms = models.ManyToManyField('Symptoms', blank=True, null=True, verbose_name = _('Symptoms'))
    valid_to_study = models.BooleanField(verbose_name=_('Valid To Study'))
    report = models.ManyToManyField('Report', blank=True, null=True, verbose_name =_('Report'))

    def __unicode__(self):
        return self.history_number

    class Meta:
        verbose_name = _(u'Clinical')
        verbose_name_plural = _(u'Clinicals')


class IllnessTranslation(models.Model):
    """ Models a illness """
    language = models.ForeignKey(Language, verbose_name=_('Language'))
    model = models.ForeignKey('Illness')

    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    type = models.CharField(max_length=255, verbose_name=_('Type'), blank=True, null=True)
    group = models.CharField(max_length=255, verbose_name=_('Group'), blank=True, null=True)

    def __unicode__(self):
        """ Show the illness name. """
        if self.name:
            return self.name
        return ''

    def save(self, *args, **kwargs):
        """ Overriding the save method, that does not support empty or repeated records."""
        try:
            if not self.name and not self.type and not self.group:
                return
            super(IllnessTranslation, self).save(*args, **kwargs)
        except Illness.DoesNotExist:
            super(IllnessTranslation, self).save(*args, **kwargs)


class Illness(MultilingualModel):
    """
    Model to store illness.
    Supports multi language.
    """
    rate_percent = models.IntegerField(verbose_name=_('Rate Percent'), blank=True, null=True)

    def __unicode__(self):
        """ Show the illness name. """
        if self.name:
            return self.name
        return ''
        
    class Meta:
        translation = IllnessTranslation
        multilingual = ['name', 'type', 'group']
        verbose_name = _(u'Illness')
        verbose_name_plural = _(u'Illnesses')


class Analisys(models.Model):
    """ Models an analisys """
    alias = models.CharField(max_length=255, verbose_name=_('Alias'), blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'))
    parameter_result = models.ManyToManyField('AnalisysParameterResult')

    def __unicode__(self):
        """ Shows the create date."""
        if self.alias:
            return self.alias
        return self.created.__str__()

    class Meta:
        verbose_name = _(u'Analisys')
        verbose_name_plural = _(u'Analyses')


class AnalisysParameterResult(models.Model):
    """ Models the parameter result from an anlisys """
    parameter = models.ForeignKey('AnalisysParameter')
    value = models.ForeignKey('ParameterValues')

    class Meta:
        verbose_name = _(u'Analisys Parameter Result')
        verbose_name_plural = _(u'Analisys Parameters Result')


class AnalisysParameterTranslation(models.Model):
    """ Models the parameter from an analisys """
    language = models.ForeignKey(Language, verbose_name=_('Language'))
    model = models.ForeignKey('AnalisysParameter')

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        """ Shows the name of a analisys parameter """
        return self.name


class AnalisysParameter(MultilingualModel):
    """
    Model to store analisysParameter.
    Supports multi language.
    """
    parameter_values = models.ManyToManyField('ParameterValues', blank=True, null=True)
    is_basic = models.BooleanField(default=False, blank=True)
    
    def __unicode__(self):
        """ Shows the name of a analisys parameter """
        return self.name

    class Meta:
        translation = AnalisysParameterTranslation
        multilingual = ['name']
        verbose_name = _(u'Analisys Parameter')
        verbose_name_plural = _(u'Analisys Parameters')


class ParameterValuesTranslation(models.Model):
    """ Models the parameter values """
    language = models.ForeignKey(Language, verbose_name=_('Language'))
    model = models.ForeignKey('ParameterValues')

    value = models.CharField(max_length=255, verbose_name=_('Value'))

    def __unicode__(self):
        """ Shows the parameter value."""
        return self.value


class ParameterValues(MultilingualModel):
    """
    Model to store parametervalues.
    Supports multi language.
    """
    pass

    def __unicode__(self):
        """ Shows the name of a analisys parameter """
        return self.value

    class Meta:
        translation = ParameterValuesTranslation
        multilingual = ['value']
        verbose_name = _(u'Parameter Value')
        verbose_name_plural = _(u'Parameter Values')


class Symptoms(models.Model):
    """ Models the symptoms """
    alias = models.CharField(max_length=255, verbose_name=_('Alias'), blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'))
    parameter_result = models.ManyToManyField('SymptomsParameterResult')

    def __unicode__(self):
        """ Shows the value symptoms."""
        if self.alias:
            return self.alias
        return self.created.__str__()

    class Meta:
        verbose_name = _(u'Symptom')
        verbose_name_plural = _(u'Symptoms')


class SymptomsParameterResult(models.Model):
    """ Models the parameter result of the symptoms """
    parameter = models.ForeignKey('SymptomsParameter')
    value = models.ForeignKey('ParameterValues')

    class Meta:
        verbose_name = _(u'Symptom Parameter Result')
        verbose_name_plural = _(u'Symptoms Parameters Result')


class SymptomsParameterTranslate(models.Model):
    """ Models the parameter of the symptoms """
    language = models.ForeignKey(Language, verbose_name=_('Language'))
    model = models.ForeignKey('SymptomsParameter')

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        """ Shows the name of the symptom """
        return self.name


class SymptomsParameter(MultilingualModel):
    """
    Model to store parametervalues.
    Supports multi language.
    """
    parameter_values = models.ManyToManyField('ParameterValues', blank=True, null=True)

    def __unicode__(self):
        """ Shows the name of the symptom """
        return self.name
    
    class Meta:
        translation = SymptomsParameterTranslate
        multilingual = ['name']
        verbose_name = _(u'Symptoms Parameter')
        verbose_name_plural = _(u'Symptoms Parameters')


class Report(models.Model):
    """ Models the reporf of a clinical case """
    alias = models.CharField(max_length=255, verbose_name=_('Alias'), blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'))
    illness = models.ManyToManyField('Illness')
    parameters = models.ManyToManyField('AnalisysParameter')

    def __unicode__(self):
        """ Shows the create date of the report."""
        if self.alias:
            return self.alias
        return self.created.__str__()

    class Meta:
        verbose_name = _(u'Report')
        verbose_name_plural = _(u'Reports')


class ForceLogoutMiddleware(object):
    """ Time to do a login to the system """
    def process_request(self, request):
        if request.user.is_authenticated() and request.user.force_logout_date and \
           ( 'LAST_LOGIN_DATE' not in request.session or \
             request.session['LAST_LOGIN_DATE'] < request.user.force_logout_date ):
            logout(request)


class MedicalProfile(models.Model):
    """ Models a medical profile """
    user = models.ForeignKey(User, unique=True)
    laboratory = models.ForeignKey("LaboratoryProfile")
    clinical = models.ManyToManyField('Clinical', blank=True, null=True)

    def __unicode__(self):
        """ Shows the username of the medical """
        return self.user.username

    class Meta:
        verbose_name = _(u'Medical Profile')
        verbose_name_plural = _(u'Medical Profiles')


class LaboratoryProfile(models.Model):
    """ Models a laboratory profile """
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        """ Shows the username of the laboratory """
        return self.user.username

    class Meta:
        verbose_name = _(u'Laboratory Profile')
        verbose_name_plural = _(u'Laboratory Profiles')











