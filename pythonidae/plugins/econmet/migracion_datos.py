# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

import csv
from plugins.econmet.utils import generate_code
from plugins.econmet.utils import convert_string
from plugins.econmet.utils import get_rate_percent
from plugins.econmet.models import *
from datetime import datetime

def process_data():
    """ Extracting information * file * and stores it in the models defined
        project
        :param file: file with csv format """
    '''
    example file:

    "ENFERMEDAD";"TIPO";"INCIDENCIA";"GRUPO ";"GASOMETRÍA";"GLUCOSA";"LACTATO";
    "LACT/PYR";"b-OH-BUT";"C. CETÓNICOS";"ORINA: ASPECTO, OLOR, COLOR";
    "ORINA:pH";"ELECTROLITOS";"AMONIO";"PERFIL HEPÁTICO";"PERFIL MUSCULAR";
    "URATO";"CALCIO";"FOSFATO";"AMINOÁCIDOS";"Cuerpos reductores";"SULFITEST";
    "HEMOGRAMA";"ÁCIDOS ORGÁNICOS";"GLICOSILACIÓN de PROTEÍNAS";
    "CARNITINA T y LIBRE";"Acil-Carnitinas";"ÁCIDOS GRASOS LIBRES";
    "Reacción de BRAND";"COAGULACIÓN";"ORÓTICO";"Lact (LCR)";
    "Sobrecarga I.V. Glucosa";"Prueba de EJERCICIO";"Prueba de AYUNO";
    "SUCCINIL-ACETONA";"a-FP";"N-Acetil-ASPARTATO ";
    " ÁCIDOS BILIARES (Cólico, pipecólico)";"Mucopolisacáridos";
    "Estudio de enfermedad peroxisomal (ácidos titánico y pristánico)";
    "d-ALA";"BIOPSIA";"MEDRO";"DIGESTIVO";"RESPIRATORIO";"HEPATOPATÍA";
    "NEUROPATÍA";"NEFROPATÍA";"CARDIOPATÍA";"OSTEO-ARTICULAR";"HEMATOLÓGICO";
    "DISMORFÍAS";"FACIAL";"PIEL-FANERAS";"OFTALMOLÓGICO";"SORDERA";
    "TRATAMIENTO";"Fenilcetonuria";;"1/10.000 ";;;;;;;;"Olor a moho";;;;;;;;;
    "Phe/Tyr > 3";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    "Fenilcetonuria";;"1/10.000 ";;;;;;;;"Olor rancio";;;;;;;;;
    "Phe/Tyr > 3";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    "Fenilcetonuria";;"1/10.000 ";;;;;;;;"Olor a ratón";;;;;;;;;
    "Phe/Tyr > 3";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    Note that the data are not specified, but are defined in the model is
    initialized to None.
    '''

    file = open("static/themes/econmet/METABOLOPATIAS20120425.csv")
    create_users()
    dicts = csv.DictReader(file, delimiter=';')
    for dict_registro in dicts:
        illness = migrate_illness(dict_registro)  # Illness
        migrate_analisysParameter(dict_registro)  # Analisys_Parameter_Values
        migrate_symptoms(dict_registro)  # Symptoms_Parameter_Values
        analisys = migrate_analisys_results(dict_registro)  # Analisys
        symptoms = migrate_symptoms_results(dict_registro)  # Symptoms
        migrate_clinical(illness, analisys, symptoms)  # Clinical


def add_analisysParameter(name, is_basic):
    """ Adds a new element to the class 'AnalisysParameter' but worthless
        :param name: param name."""
    if name:
        try:
            return AnalisysParameterTranslation.objects.get(name=name).model
        except AnalisysParameterTranslation.DoesNotExist:
            pass
        es = Language.objects.get(code='es')
        analisysparameter = AnalisysParameter.objects.create(is_basic=is_basic)
        AnalisysParameterTranslation.objects.create(language=es, model=analisysparameter, name=name)
        return analisysparameter


def add_symptomsParameter(name):
    """ Adds a new element to the class 'SymptomsParameter' but worthless
        :param name: param name."""
    if name:
        try:
            return SymptomsParameterTranslate.objects.get(name=name).model
        except SymptomsParameterTranslate.DoesNotExist:
            pass
        es = Language.objects.get(code='es')
        symptomsparameter = SymptomsParameter.objects.create()
        SymptomsParameterTranslate.objects.create(language=es, model=symptomsparameter, name=name)
        return symptomsparameter 


def add_ParameterValues(value):
    """ Adds a new element to the class 'ParameterValues' but worthless
        :param value: param value."""
    if value:
        try:
            parameterValuesTranslation = ParameterValuesTranslation.objects.get(value=value)
            return parameterValuesTranslation.model
        except ParameterValuesTranslation.DoesNotExist:
            pass
        es = Language.objects.get(code='es')
        parameter = ParameterValues.objects.create()
        ParameterValuesTranslation.objects.create(language = es, model = parameter, value=value)
        return parameter


def migrate_illness(dict_registro):
    """ Adds a new element to the class 'Illness'
        :param dict_registro: registry data file."""

    name, type, rate, rate_percent, group = None, None, None, None, None
    if dict_registro['ENFERMEDAD'] != '':
        name = dict_registro['ENFERMEDAD']
    if dict_registro['TIPO'] != '' and dict_registro['TIPO'] != ' ':
        type = dict_registro['TIPO']
    if dict_registro['INCIDENCIA'] != '':
        rate = dict_registro['INCIDENCIA']
        rate_percent = get_rate_percent(rate)
    if dict_registro['GRUPO '] != '':
        group = dict_registro['GRUPO ']

    try:
        illnessTranslation = IllnessTranslation.objects.get(name=name, type=type, group=group)
        if illnessTranslation:
            return illnessTranslation.model
    except IllnessTranslation.DoesNotExist or Illness.DoesNotExist:
        pass
    if name or type or group:
        es = Language.objects.get(code='es')
        illness = Illness.objects.create(rate_percent=rate_percent)
        IllnessTranslation.objects.create(language=es, model=illness, name=name, type=type, group=group) 
        if illness.id:
            return illness
    return None


def migrate_analisysParameter(dict_registro):
    """ Adds a new element to the class 'AnalisysParameter'
        :param dict_registro: registry data file."""

    analisys_parameters_basic = ['GASOMETRÍA','GLUCOSA','LACTATO','LACT/PYR','b-OH-BUT','C. CETÓNICOS','b-OH-BUT/Acetoacetato',
                                 'ORINA: ASPECTO, OLOR, COLOR','ORINA: pH','Glucosuria','ELECTROLITOS','AMONIO','PERFIL HEPÁTICO',
                                 'PERFIL MUSCULAR','PERFIL LIPÍDICO','URATO','CALCIO','FOSFATO','AMINOÁCIDOS','Cuerpos reductores',
                                 'HEMOGRAMA','ÁCIDOS ORGÁNICOS','GLICOSILACIÓN de PROTEÍNAS','Perfil renal','CARNITINA T y LIBRE',
                                 'Glucosa/Insulina','Cortisol y GH']
    analisys_parameters = ['Tiroides','Perfil hipofisario','Acil-Carnitinas','ÁCIDOS GRASOS LIBRES','COAGULACIÓN','SULFITEST',
                           'Reacción de BRAND','Lact (LCR)','Aminoácidos (LCR)','Sobrecarga Glucosa','Prueba de EJERCICIO',
                           'Prueba de AYUNO','Prueba del glucagón (después de un ayuno de 12 h)','SUCCINIL-ACETONA','a-FP',
                           'N-Acetil-ASPARTATO ',' ÁCIDOS BILIARES (Cólico, pipecólico)','Mucopolisacáridos','Oligosacáridos',
                           'Estudio de enfermedad peroxisomal (ácidos fitánico y pristánico)','BIOTINA (orina)','BIOTINIDASA',
                           'd-ALA','Test de SAICAR','NEUROTRANSMISORES','Sobrecarga de Fenilalanina','Guanidino-acetato (creatina)','BIOPSIA']    

    for analisys_parameter in analisys_parameters_basic:
        add_analisysParameter(analisys_parameter, True)
        if dict_registro[analisys_parameter] != '' and dict_registro[analisys_parameter] != ' ':
            parameter = add_ParameterValues(convert_string(dict_registro[analisys_parameter])) 
            if not parameter.id:
                parameter = ParameterValuesTranslation.objects.get(value=convert_string(dict_registro[analisys_parameter])).model
            AnalisysParameterTranslation.objects.get(name=analisys_parameter).model.parameter_values.add(parameter)

    for analisys_parameter in analisys_parameters:
        add_analisysParameter(analisys_parameter, False)
        if dict_registro[analisys_parameter] != '' and dict_registro[analisys_parameter] != ' ':
            parameter = add_ParameterValues(convert_string(dict_registro[analisys_parameter]))
            if not parameter.id:
                parameter = ParameterValuesTranslation.objects.get(value=convert_string(dict_registro[analisys_parameter])).model
            AnalisysParameterTranslation.objects.get(name=analisys_parameter).model.parameter_values.add(parameter)


def migrate_symptoms(dict_registro):
    """ Adds a new element to the class 'SymptomsParameter'
        :param dict_registro: registry data file."""    
    symptoms_parameters = ['MEDRO','DIGESTIVO','RESPIRATORIO','HEPATOPATÍA','NEUROPATÍA','NEFROPATÍA',
                           'CARDIOPATÍA','MIOPATÍA','OSTEO-ARTICULAR','HEMATOLÓGICO','DISMORFÍAS',
                           'FACIAL','PIEL-FANERAS','OFTALMOLÓGICO','SORDERA','SISTEMA INMUNOLÓGICO']

    for symptoms_parameter in symptoms_parameters:
        add_symptomsParameter(symptoms_parameter)
        if dict_registro[symptoms_parameter] != '' and dict_registro[symptoms_parameter] != ' ':
            parameter = add_ParameterValues(convert_string(dict_registro[symptoms_parameter]))
            if not parameter.id:
                parameter = ParameterValuesTranslation.objects.get(value=convert_string(dict_registro[symptoms_parameter])).model
            SymptomsParameterTranslate.objects.get(name=symptoms_parameter).model.parameter_values.add(parameter)


def migrate_analisys_results(dict_registro):
    """ Adds a new element to the class 'Analisys'
        :param dict_registro: registry data file."""

    analisys_parameters = ['GASOMETRÍA','GLUCOSA','LACTATO','LACT/PYR','b-OH-BUT','C. CETÓNICOS','b-OH-BUT/Acetoacetato',
                                 'ORINA: ASPECTO, OLOR, COLOR','ORINA: pH','Glucosuria','ELECTROLITOS','AMONIO','PERFIL HEPÁTICO',
                                 'PERFIL MUSCULAR','PERFIL LIPÍDICO','URATO','CALCIO','FOSFATO','AMINOÁCIDOS','Cuerpos reductores',
                                 'HEMOGRAMA','ÁCIDOS ORGÁNICOS','GLICOSILACIÓN de PROTEÍNAS','Perfil renal','CARNITINA T y LIBRE',
                                 'Glucosa/Insulina','Cortisol y GH','Tiroides','Perfil hipofisario','Acil-Carnitinas',
                                 'ÁCIDOS GRASOS LIBRES','COAGULACIÓN','SULFITEST', 'Reacción de BRAND','Lact (LCR)','Aminoácidos (LCR)',
                                 'Sobrecarga Glucosa','Prueba de EJERCICIO', 'Prueba de AYUNO','Prueba del glucagón (después de un ayuno de 12 h)',
                                 'SUCCINIL-ACETONA','a-FP', 'N-Acetil-ASPARTATO ',' ÁCIDOS BILIARES (Cólico, pipecólico)',
                                 'Mucopolisacáridos','Oligosacáridos', 'Estudio de enfermedad peroxisomal (ácidos fitánico y pristánico)',
                                 'BIOTINA (orina)','BIOTINIDASA', 'd-ALA','Test de SAICAR','NEUROTRANSMISORES','Sobrecarga de Fenilalanina',
                                 'Guanidino-acetato (creatina)','BIOPSIA']

    analisys = None
    for analisys_parameter in analisys_parameters:
        if dict_registro[analisys_parameter] != '' and dict_registro[analisys_parameter] != ' ':
            parameter = AnalisysParameterTranslation.objects.get(name=analisys_parameter).model
            value = ParameterValuesTranslation.objects.get(value=dict_registro[analisys_parameter]).model
            analisys_parameter_result = AnalisysParameterResult.objects.create(parameter=parameter, value=value)
            if analisys_parameter_result.id:
                if analisys:
                    analisys.parameter_result.add(analisys_parameter_result)
                else:
                    analisys = Analisys.objects.create(created=datetime.now())
                    analisys.parameter_result.add(analisys_parameter_result)
    return analisys


def migrate_symptoms_results(dict_registro):
    """ Adds a new element to the class 'Symptoms'
        :param dict_registro: registry data file."""
    symptoms_parameters = ['MEDRO','DIGESTIVO','RESPIRATORIO','HEPATOPATÍA','NEUROPATÍA','NEFROPATÍA',
                           'CARDIOPATÍA','MIOPATÍA','OSTEO-ARTICULAR','HEMATOLÓGICO','DISMORFÍAS',
                           'FACIAL','PIEL-FANERAS','OFTALMOLÓGICO','SORDERA','SISTEMA INMUNOLÓGICO']

    symptoms = None
    for symptoms_parameter in symptoms_parameters:
        if dict_registro[symptoms_parameter] != '' and dict_registro[symptoms_parameter] != ' ':
            parameter = SymptomsParameterTranslate.objects.get(name=symptoms_parameter).model
            value = ParameterValuesTranslation.objects.get(value=dict_registro[symptoms_parameter]).model
            symptoms_parameter_result = SymptomsParameterResult.objects.create(parameter=parameter, value=value)
            if symptoms_parameter_result.id:
                if symptoms:
                    symptoms.parameter_result.add(symptoms_parameter_result)
                else:
                    symptoms = Symptoms.objects.create(created=datetime.now())
                    symptoms.parameter_result.add(symptoms_parameter_result)
    return symptoms


def migrate_clinical(illness, analisys, symptoms):
    """ Adds a new element to the class 'Clinical'
        :param dict_registro: registry data file.
        :param illness: reference to the class `illness`.
        :param analisys: reference to the class `analisys`
        :param symptoms: reference to the class `symptoms`"""

    medical = MedicalProfile.objects.get(id=1)
    find = False
    for clinical in Clinical.objects.all():
        if illness in clinical.illness.filter():
            if analisys:
                clinical.analisys.add(analisys)
            if symptoms:
                clinical.symptoms.add(symptoms)
            clinical.save()
            find = True
            return 
    if not find and (illness or analisys or symptoms):
        clinical = Clinical.objects.create(history_number=generate_code(), valid_to_study=True)
        if illness:
            clinical.illness.add(illness)
        if analisys:
            clinical.analisys.add(analisys)
        if symptoms:
            clinical.symptoms.add(symptoms)
        clinical.save()
        medical.clinical.add(clinical)


def create_users():
    """ Create a user profile for Laboratory and one for the Medical Profile """

    laboratory = User.objects.create_user('laboratorio', 'laboratorio@correo.es', '123')
    laboratory.first_name = 'Laboratorio'
    laboratory.last_name = 'Granada'
    laboratory_profile = LaboratoryProfile.objects.create(user=laboratory)

    medical = User.objects.create_user('medico', 'medico@correo.es', '123')
    medical.first_name = 'Medico'
    medical.last_name = 'Granada'
    MedicalProfile.objects.create(user=medical, laboratory=laboratory_profile)

 
def delete_users():
     """ Delete the users created for the profile and Medical Laboratory """

     laboratory = User.objects.get(username='laboratorio')
     laboratory.delete()
     
     medical = User.objects.get(username='medico')
     medical.delete()
    
        
