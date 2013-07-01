# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from plugins.econmet.models import Clinical, Illness, AnalisysParameter
from plugins.econmet.models import ParameterValues, SymptomsParameter
from plugins.econmet.models import Report, MedicalProfile, LaboratoryProfile
from plugins.econmet.models import IllnessTranslation
from plugins.econmet.models import AnalisysParameterTranslation
from plugins.econmet.models import ParameterValuesTranslation
from plugins.econmet.models import SymptomsParameterTranslate
from django.contrib import admin


""" Translation Class """


class IllnessTranslationInline(admin.StackedInline):
    model = IllnessTranslation
    extra = 1
    min_num = 1


class AnalisysParameterTranslationInline(admin.StackedInline):
    model = AnalisysParameterTranslation
    extra = 1
    min_num = 1


class ParameterValuesTranslationInline(admin.StackedInline):
    model = ParameterValuesTranslation
    extra = 1
    min_num = 1


class SymptomsParameterTranslateInline(admin.StackedInline):
    model = SymptomsParameterTranslate
    extra = 1
    min_num = 1


""" Class models to customize """


class ClinicalAdmin(admin.ModelAdmin):
    filter_horizontal = ['illness', 'analisys', 'symptoms', 'report']


class AnalisysParameterAdmin(admin.ModelAdmin):
    inlines = [AnalisysParameterTranslationInline]
    filter_vertical = ['parameter_values']


class SymptomsParameterAdmin(admin.ModelAdmin):
    filter_vertical = ['parameter_values']
    inlines = [SymptomsParameterTranslateInline]


class MedicalProfileAdmin(admin.ModelAdmin):
    filter_vertical = ['clinical']


class IllnessAdmin(admin.ModelAdmin):
    inlines = [IllnessTranslationInline]


class ParameterValuesAdmin(admin.ModelAdmin):
    inlines = [ParameterValuesTranslationInline]
    
class ReportAdmin(admin.ModelAdmin):
    filter_horizontal = ['illness', 'parameters']

""" Econmet models created in order to visualize from the admin interface """
admin.site.register(Clinical, ClinicalAdmin)
admin.site.register(Illness, IllnessAdmin)
admin.site.register(AnalisysParameter, AnalisysParameterAdmin)
admin.site.register(ParameterValues, ParameterValuesAdmin)
admin.site.register(SymptomsParameter, SymptomsParameterAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(MedicalProfile,MedicalProfileAdmin)
admin.site.register(LaboratoryProfile)
