# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from plugins.econmet.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from datetime import datetime
from collections import defaultdict

def convert_string(text):
    """ Convert from string to uft-8. 
        :param text: text to convert. """
    try:
        unicode = text.decode("utf-8")
    except UnicodeDecodeError:
        unicode = text.decode("cp1252")
    return unicode    
    
def generate_code():
    """ Generates a random string of caracteres."""
    import random
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'#'abcdefghijklmnopqrstuvwxyz'
    min = 5
    max = 15
    string=''
    for x in random.sample(alphabet,random.randint(min,max)):
        string+=x
    return string


def get_rate_percent(text):
    """ Calculate the percent of the rate """
    matchs = re.findall("\d/\d+.\d+",text)
    count = 0
    i = 1
    for match in matchs:
        element = match.split('/')
        count = (count + (int(element[0])/float(element[1]))*100)/i
        i += 1
    return count 

def get_data_object(object,elements):
    """ Returns a dictionary with the values of the object """
    dict = {}
    if object:
        for element in elements['fields']:
            dict[element] = object.__getattribute__(element)
        for element in elements['m2m']:
            if object.__getattribute__(element).values().__len__() > 0:
                if element == 'report':
                    dict[element] = get_data_report(object.__getattribute__('report'), models.get_model('econmet', 'report'))
                elif element == 'illness':
                    dict[element] = get_data_illness(object.__getattribute__(element), models.get_model('econmet', element))
                else:
                    dict[element] = get_data(object.__getattribute__(element), models.get_model('econmet', element))
            else:
                dict[element] = get_data("", models.get_model('econmet',element))
    
    return dict

def get_data_report(object, model):
    """ Returns a dictionary with the values of the object report """
    dict = {}
    if object:
        dict['name'] = object.model._meta.module_name
        dict['data'] = {}
        for field in object.model._meta.fields:
            #dict['data'].append({'name': field.get_attname(), 'value' : object.values()[0][field.name]})
            dict['data'][field.get_attname()] = (object.latest('created').__dict__[field.name] or '')

        dict['illness'] = []
        dict['parameters'] = []
        obj = object.latest('created')
        for illness in list(obj.illness.all()):
            list_element = []
            for field in IllnessTranslation._meta.fields:
                if field.name == 'name' or field.name == 'group' or field.name == 'type':
                    list_element.append({'name': field.get_attname(), 'value': illness.illnesstranslation_set.values_list(field.name, flat=True)[0]})
            dict['illness'].append(list_element)
        list_element = []
        for parameter in list(obj.parameters.all()):
            list_element.append(parameter.name)
        dict['parameters'].append(list_element)

    else:
        dict['name'] = model._meta.module_name
        dict['data'] = []
        for field in model._meta.fields:
            dict['data'].append({'name': field.get_attname(), 'value' : ''})

    return dict

def get_data_illness(object, model):
    """ Returns a dictionary with the values of the object illness"""
    dict = {}   
    if object:
        dict['name'] = object.model._meta.module_name
        dict['data'] = []
        for object_id in object.values_list('id', flat=True):
            aux_data = []
            if 'multilingual' in object.model._meta.__dict__:
                    translation = object.model._meta.translation.objects.get(model=object_id)
                    for field in object.model._meta.multilingual:
                        aux_data.append({'name': field, 'value' : translation.__dict__[field]})
            for field in object.model._meta.fields:
                if field.verbose_name != 'ID':
                    aux_data.append({'name': field.get_attname(), 'value' : object.get(id=object_id).__dict__[field.name]})
            dict['data'].append(aux_data)
    return dict        

    
def get_data(object, model):
    """ Returns a dictionary with the values of the object """
    dict = {}
   
    if object:
        dict['name'] = object.model._meta.module_name
        dict['data'] = []
        if 'multilingual' in object.model._meta.__dict__:
            object_id = int(object.values_list('id', flat=True)[0])
            translation = object.model._meta.translation.objects.get(model=object_id)
            for field in object.model._meta.multilingual:
                dict['data'].append({'name': field, 'value' : translation.__dict__[field]})
        for field in object.model._meta.fields:
            if field.verbose_name != 'ID':
                dict['data'].append({'name': field.get_attname(), 'value' : object.values()[0][field.name]})
        
        if object.model._meta.many_to_many.__len__() > 0:
            dict['relation'] = []
            for obj in object.filter():
                list_element = []
                for m2m_element in model._meta.many_to_many:
                    for element in list(obj.__getattribute__(m2m_element.name).all()):
                        added = 0
                        for el in list_element:
                            if el['name'] == element.parameter.name:
                                el['value'].append(element.value)
                                added = 1
                        if added == 0:
                            list_element.append({'name': element.parameter.name, 'value' :[element.value]})
                dict['relation'].append({'id': obj.id, 'data': list_element})

    else:
        dict['name'] = model._meta.module_name
        dict['data'] = []
        fields = model._meta.fields
        if 'multilingual' in model._meta.__dict__:
            fields = model._meta.multilingual + fields
        for field in fields:
            name = field if type(field) == type('') else field.get_attname()
            dict['data'].append({'name': name, 'value' : ''})

    return dict


def get_dict_data(objects, model, info_field=None, is_valid=False):
    """ Get the object values and convert into a dictionary """
    if model._meta._many_to_many().__len__() == 0 :
        dict_data = {}
        fields = model._meta.fields
        for field in fields:
            if field.name != 'id':
                for object in objects:
                    dict_data[field.name] = object.__getattribute__(model._meta.module_name).values_list(field.name, flat=True).order_by(field.name).distinct(field.name)
        return dict_data
    else:
        fields = model._meta.many_to_many
        dict_data = []
        for object in objects:
            if is_valid:
                datas = list(object.__getattribute__(model._meta.module_name).exclude(valid_to_study=False).values())
            else:
                datas = list(object.__getattribute__(model._meta.module_name).values())
            for data in datas:
                for field in fields:
                    if field.name not in data and 'id' in data:
                        data[field.name] = get_info_field_data(object.__getattribute__(model._meta.module_name).get(id = data['id']).__getattribute__(field.name).all())
#                        data[field.name] = object.__getattribute__(model._meta.module_name).get(id = data['id']).__getattribute__(field.name).values_list('id',info_field[field.name])
#                        import pdb; pdb.set_trace()
#                        for info_field_element in info_field[field.name]:
#                            data_aux = 
#                            if data['history_number'] == 'Prueba':
#                                import pdb; pdb.set_trace()
#                            if data_aux and data_aux[0]:
#                                data[field.name] = object.__getattribute__(model._meta.module_name).get(id = data['id']).__getattribute__(field.name).values_list('id',info_field_element)
#                                break
                dict_data.append(data)
        return dict_data
    
def get_info_field_data(data):
    """ Get the coherent value from the info field """
    result = []    
    for element in data:
        result.append((element.id, element.__str__()))
    return result
    
def get_dict_specific_data(objects, model, info_field=None):
    """ Get the object values and convert into a dictionary """
    if model._meta._many_to_many().__len__() == 0 :
        dict_data = {}
        fields = model._meta.fields
        for field in fields:
            if field.name != 'id':
                for object in objects:
                    dict_data[field.name] = object.values_list(field.name, flat=True).order_by(field.name).distinct(field.name)
        return dict_data
    else:
        fields = model._meta.many_to_many
        dict_data = []
        datas = list(objects.values())
        for data in datas:
            for field in fields:
                if field.name not in data and 'id' in data:
                    data[field.name] = model.objects.get(id = data['id']).__getattribute__(field.name).values_list('id',info_field[field.name])
            dict_data.append(data)
        return dict_data
    

def createuser(values):
    """ Create a user """
    newUser = User()
    newUser.username = values['username']
    newUser.first_name = values['name']
    newUser.last_name = values['surname']
    newUser.email = values['mail']
    newUser.set_password(values['password'])
    newUser.save()
    return newUser


def get_values(fields, model):
    """ Get a dictionary with the fields pass as parameters """
    data = []
    for field in sorted(fields):
        name = field
        value = model.objects.get(name=field).model.parameter_values.order_by('parametervaluestranslation__value').values_list('parametervaluestranslation__value', flat=True)
        data.append({'name': name, 'values': value})
    return data

def clean_dict(data):
    """ Delete empty tuplas from a dictionary """
    dict = {}
    for element in data.lists():
        if len(element[1]) > 1 and element[0] != 'csrfmiddlewaretoken' and element[0] != 'clinical_id' and element[0] != 'analisys_type':
            dict[element[0]] = element[1]
    return dict


def get_profile_name(user):
    """ Get the profile name from a user """
    if user.laboratoryprofile_set.exists():
        return user.laboratoryprofile_set.reverse()[0]._meta.module_name
    elif user.medicalprofile_set.exists():
        return user.medicalprofile_set.reverse()[0]._meta.module_name
    elif user.is_staff:
        return 'Admin'
    
def get_profile(user):
    """ Get the profile from a user """
    if user.laboratoryprofile_set.exists():
        return user.laboratoryprofile_set.reverse()
    elif user.medicalprofile_set.exists():
        return user.medicalprofile_set.reverse()
    elif user.is_staff:
        return MedicalProfile.objects.all()
 

def get_symptoms_parameters(clinical):
    """ Get a list with the params from symptoms' clinical """
    parameters = []
    for symptom in list(clinical.symptoms.all()):
        for parameter_result in list(symptom.parameter_result.all()):
            parameters.append(parameter_result.value_id)
    return set(parameters)

def get_analisys_parameters(clinical):
    """ Get a list with the params from analisys' clinical """
    parameters = []
    for analisys in list(clinical.analisys.all()):
        for parameter_result in list(analisys.parameter_result.all()):
            parameters.append(parameter_result)
    return organize_analysis_parameter_result(parameters)

def organize_analysis_parameter_result(parameters):
    d = defaultdict(list)
#    import pdb; pdb.set_trace()
    for parameter in parameters:
        if d.has_key(parameter.parameter.id):
            d[parameter.parameter.id].append(parameter.value.id)
        else:
            d[parameter.parameter.id] = [parameter.value.id]
    #import pdb; pdb.set_trace()
    return d

def get_best_matches(data, num):
    """ Get the num best matches from the set data """
    if data.__len__() <= num:
        num = data.__len__()

    count = 0;
    matches = []
    while count < num:
        matches.append(data[count])
        count += 1
    return matches
        
def get_commun_clinical(clinicals):
    """ Get the clinicial, commons in filtered by parameter """
    result = clinicals[0]
    for clinical in clinicals:
        result = result and clinical
    return result        
            
def get_inferences_clinicals(clinical):
    """ Get the clinical that content any of the symptoms or analisys from the clinical pass as reference """
    dictio = get_analisys_parameters(clinical)
    max_local = 0
    max_clinic = 0
    res = {}
    for clinic in Clinical.objects.all():
        if clinic.illness != None:
            for analisys in clinic.analisys.all():
                for parameter in dictio.keys():
                    try:
                        param = analisys.parameter_result.get(parameter=parameter)
                        if param.value.id in dictio.get(parameter):
                            max_local = max_local + 1
                    except:
                        pass
                if max_local > max_clinic:
                    max_clinic = max_local
                max_local = 0
            res[clinic.history_number] = max_clinic
            max_clinic = 0
            
            for symptom in clinic.symptoms.all():
                for parameter in dictio.keys():
                    try:
                        param = symptom.parameter_result.get(parameter=parameter)
                        if param.value.id in dictio.get(parameter):
                            max_local = max_local + 1
                    except:
                        pass
                if max_local > max_clinic:
                    max_clinic = max_local
                max_local = 0
            res[clinic.history_number] = max_clinic + res[clinic.history_number]
            max_clinic = 0

    res = sorted(res, key=res.get, reverse=True)
    result = []
    for i in range(0, len(res)):
        result.append(Clinical.objects.get(history_number=res[i]))
   
    return result


def save_report(clinicals):
    """ Convert from clinical to Report object """
    report = Report.objects.create(created = datetime.now())
    for clinical in clinicals:
        for illness in list(clinical.illness.all()):
            report.illness.add(illness)
        for analisys in list(clinical.analisys.all()):
            for parameter_result in list(analisys.parameter_result.filter(parameter__is_basic=False)):
                report.parameters.add(parameter_result.parameter)
    return report
     
            
def generate_report(clinical):
    """ Generate a report and asociate to a clinical """
    inferences = get_inferences_clinicals(clinical)
    matches = get_best_matches(inferences, 4)
    report = save_report(matches)
    clinical.report.add(report)
      
