# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.forms import ModelForm
from plugins.econmet.models import *
from django import forms
from django.core import validators
from django.contrib.auth.models import User

class IllnessForm(ModelForm):
    """ Form class `Illness`"""
    class Meta:
        model = Illness
        
        
class ClinicalForm(ModelForm):
    """ Form class `Clinical`"""
    class Meta:
        model = Clinical
        

class MedicalForm(ModelForm):
    """ Form class 'Medical'"""
    class Meta:
        model = MedicalProfile
 
class LaboratoryForm(ModelForm):
    """ Form class 'Laboratory'"""
    class Meta:        
        model = LaboratoryProfile    
        
class SymptomsForm(ModelForm):
    """ Form class 'Symptoms' """
    class Meta:
        model = Symptoms

        
        
        
        
        