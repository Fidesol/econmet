# -*- coding: utf-8 -*-
__autor__ = "Maria del Mar Jiménez Torres, Fundación I+D del Software Libre"
__email__ = "mjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from _mysql_exceptions import IntegrityError
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from plugins.econmet.models import *
from plugins.econmet.forms import *
from plugins.econmet.utils import *


def error_404_view(request):
    """ Custom 404 error view """
    return render(request, '404.html', {
                                        'title': _('404 error'),
    })


def error_500_view(request):
    """ Custom 500 error view """
    return render(request, '500.html', {
                                        'title': _('500 error'),
    })   

def register(request, profile = None):
    """ register user view """
    fields = [{'verbose_name': _('Username'), 'name' : 'username'}, {'verbose_name':_('Password') , 'name' : 'password'}, {'verbose_name':_('Confirm password') , 'name' : 'confirm password'},
              {'verbose_name':_('Mail'),  'name' : 'mail'}, {'verbose_name':_('Confirm mail') , 'name' : 'confirm mail'}, {'verbose_name':_('Name') , 'name' : 'name'},
              {'verbose_name':_('Surname') , 'name' : 'surname'}, {'verbose_name':_('Laboratory'), 'name' : 'laboratory'}]
    defect_profile = 'laboratory'
    laboratory_list = None
    if profile and profile != defect_profile:
        defect_profile = profile
        laboratory_list = list(LaboratoryProfile.objects.all())
  
    if request.method == 'POST':
        #Check if the user exists in the database from username field
        post_values = request.POST.copy()
        try:
            User.objects.get(username = request.POST['username'])
            post_values['password'] = ''
            username = post_values['username']
            post_values['username'] = ''
            return render(request, 'register.html',{
                                                    'title' : _('Econmet'),
                                                    'profile_type' : defect_profile,
                                                    'fields' : fields,
                                                    'laboratory_list': laboratory_list,                                                    
                                                    'values': post_values,
                                                    'error_message' : _('Username ') +username +_(' already exists.')
                                                    })
            
        except:
            pass
        
        newUser = createuser(request.POST)
        post_values = request.POST.copy()
        post_values['user'] = newUser.id
        if request.POST['profile_type'] == 'laboratory':
            form = LaboratoryForm(post_values)
        else:
            form = MedicalForm(post_values)
        
        if form.is_valid():
            form.save()
            return render(request, 'econmet/home.html', {
                                                  'title': _('Econmet'),                                 
                                                })         
  
    return render(request,'register.html',{
                                               'title' : _('Econmet'),
                                               'profile_type' : defect_profile,
                                               'fields' : fields,
                                               'laboratory_list': laboratory_list,
                                               'values' : {},
                                               })

def mylogin(request):
    """ Login a user session in the system """
    error_message = None
    LaboratoryProfile
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect(reverse('clinical_view'))
        else:
            error_message = _("Incorrect User o Pass") 
    return render(request, 'econmet/home.html', {
                                          'title': _('Econmet'),                                          
                                          'error_message' : error_message,
    })

 
def logout(request, next_page=None, template_name='registration/logged_out.html', redirect_field_name=logout):
    """  Close a user session """ 
    logout(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        return HttpResponseRedirect(redirect_to)
    elif next_page is None:
        return render_to_response(template_name,
                                  {'title': _('Logged out')},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(next_page or request.path)
           
    
@login_required    
def illness(request, id=None):
    """ Illness view """
    illness_element = None
    dict_illness_element = None
    message = None
    id_to_edit = None

    if id:
        illness_element = get_object_or_404(Illness, pk=id)
        dict_illness_element = illness_element.__dict__
        id_to_edit = id
        
    if id and 'delete' in request.GET:
        illness_element.delete()
        message = _('Illness deleted sucessfully.')
        request.session['message'] = message
        id_to_edit = None        
        return redirect(reverse,('illness_view')+'?page='+request.GET['page'])
        
    if request.method == 'POST':
        if 'id' in request.POST:
            edit_illness = IllnessForm(request.POST, instance=illness_element)
            edit_illness.save()
            message = _('Illness ') + edit_illness.data['name'] + _(' changed sucessfully.')
            request.session['message'] = message
            return redirect(reverse('illness_view')+'?page='+request.GET['page'])
        new_illness = IllnessForm(request.POST)
        new_illness.save()
        message =_('Illness ') + new_illness.data['name'] + _(' added sucessfully.')
        request.session['message'] = message
        return redirect(reverse('illness_view')+'?page='+request.GET['page'])
    
    if request.session.has_key('message'):
        message = request.session['message']
        request.session.pop('message')

    return render_to_response('illness.html', {
                                                'title' : _('Illness'),
                                                'verbose_model' : _('illness'),
                                                'fields' : Illness._meta.fields,
                                                'object_model' : define_pagination(request, Illness.objects.values()),
                                                'object_element' : dict_illness_element,
                                                'data' : get_dict_data(Illness),
                                                'id_to_edit' : id_to_edit,
                                                'message' : message,
                                                'divided': 'yes',
                                                'nav_illness' : True, 
                                                },
                                                context_instance=RequestContext(request))
    


@login_required
def clinical(request):
    """ Clinical view """
    m2m_fields = Clinical._meta.many_to_many
    nav_field_active = m2m_fields[0].name
    is_valid = 'valid' in request.GET
        
    elements = {'fields': ['id','history_number'], 'm2m': [nav_field_active]}
    
    if 'status' in request.GET and 'new' in request.GET['status']:
        return render_to_response('thumb-view.html',{
                                                         'nav_clinical' : True,
                                                         'title' : _('Clinical'),
                                                         'verbose_model' : Clinical._meta.verbose_name,
                                                         'module_name' : Clinical._meta.module_name,
                                                         'm2m_fields' :m2m_fields,
                                                         'data_object' : [],
                                                         'new' : True,
                                                         'profile': get_profile_name(request.user), 
                                                         },
                                                         context_instance=RequestContext(request))
        

    profile = get_profile(request.user)
    if request.user.laboratoryprofile_set.exists():
        profile = profile[0].medicalprofile_set.reverse()
    clinical = []
    for clinic in Clinical.objects.all():
        if clinic.illness.all():
            name = clinic.illness.all()[0].name
        else :
            name = ''
        clinical.append({'id':clinic.id,'history_number':clinic.history_number,'illness':name, 'analisys':len(Analisys.objects.filter(clinical = clinic)), 'symptoms':len(Symptoms.objects.filter(clinical = clinic)), 'report':len(Report.objects.filter(clinical = clinic))})
    #clinical = get_dict_data(profile,Clinical,{'illness': 'illnesstranslation__name', 'analisys': 'created', 'symptoms': 'created', 'report': 'created'}, is_valid)
    
    error_message = None
    if request.session.has_key('message'):
        error_message = request.session['message']
        request.session.pop('message')
    
    return render_to_response('clinical_list.html', {
                                                'nav_clinical' : not is_valid, 
                                                'title' : _('Clinical'),
                                                'verbose_model' : Clinical._meta.verbose_name,
                                                'module_name' : Clinical._meta.module_name,
                                                'fields' : Clinical._meta.fields + Clinical._meta.many_to_many,
                                                'object_model' : clinical,
                                                'divided': 'yes', 
                                                'profile': get_profile_name(request.user),
                                                'error_message': error_message,
                                                'is_valid': is_valid,                                                
                                                },
                                                context_instance=RequestContext(request))  

  
        
@login_required
def thumb_view(request, id=None, element=None):
    """ specific clinical view """
    if id: 
        clinical = get_object_or_404(Clinical, pk=id)
    else:
        clinical = None
    
    m2m_fields = Clinical._meta.many_to_many
    nav_field_active = m2m_fields[1].name
    if element:
        nav_field_active = element
    
    template = 'thumb-view.html'    
    if element == 'report':
        template = 'report-view.html'
        
    message = None    
    if request.session.has_key('message'):
        message = request.session['message']
        request.session.pop('message')
    
    return render_to_response(template,{
                                         'nav_clinical' : True, 
                                         'nav_field_active': nav_field_active,
                                         'title' : _('Clinical'),
                                         'verbose_model' : Clinical._meta.verbose_name,
                                         'module_name' : Clinical._meta.module_name,
                                         'm2m_fields': m2m_fields,
                                         'element' : element,
                                         'data_object' : get_data_object(clinical, {'fields': ['id','history_number'], 'm2m': [nav_field_active]}),
                                         'new' : False,
                                         'profile': get_profile_name(request.user),
                                         'message': message,
                                         },
                                        context_instance=RequestContext(request))

@login_required
def search(request):
    """ Search a Clinical by history number """
    if request.method == 'POST':
        str_to_find = request.POST['search']
    else:
        str_to_find = request.GET['search']
        
    clinical = Clinical.objects.filter(history_number__contains=str_to_find)
    if clinical.__len__() == 0:
        request.session['message'] = unicode(_('Search '))+request.POST['search']+ unicode(_(' not found'))
        return redirect(reverse('clinical_view'))
    if clinical.__len__() > 1:
        clinical = get_dict_specific_data(clinical, Clinical, {'illness': 'illnesstranslation__name', 'analisys': 'created', 'symptoms': 'created', 'report': 'created'})
        return render_to_response('clinical_list.html', {
                                                    'nav_clinical' : True, 
                                                    'title' : _('Clinical'),
                                                    'verbose_model' : Clinical._meta.verbose_name,
                                                    'module_name' : Clinical._meta.module_name,
                                                    'fields' : Clinical._meta.fields + Clinical._meta.many_to_many,
                                                    'object_model' : clinical,
                                                    'divided': 'yes', 
                                                    'profile': get_profile_name(request.user),
                                                    'search': str_to_find,                                              
                                                    },
                                                    context_instance=RequestContext(request))                  
    return redirect('/econmet/clinical/'+str(clinical[0].id))

        
@login_required
def symptoms(request):
    """ Symptoms view """
    error_message = None
    clinical = None

    if request.method == 'POST':
        if 'history_number' in request.POST:
            if 'clinical_id' in request.POST and request.POST['clinical_id'] != '':
                clinical = Clinical.objects.get(id=request.POST['clinical_id'])
            else:
                clinical = Clinical.objects.create(history_number = request.POST['history_number'], valid_to_study=False)
                if request.user.medicalprofile_set.exists():
                    profile = request.user.medicalprofile_set.reverse()[0]
                    profile.clinical.add(clinical)
        else:
            clinical = Clinical.objects.get(id=request.POST['clinical_id'])
            data = clean_dict(request.POST)
            if len(data) > 0:
                symptoms = Symptoms.objects.create(created = datetime.now(), alias=request.POST.get('alias', ''))
                clinical.symptoms.add(symptoms)
                for element in data:
                    if element != 'alias':
                        parameter = SymptomsParameterTranslate.objects.get(name=element).model
                        value = ParameterValuesTranslation.objects.get(value=data[element][0]).model
                        symptoms.parameter_result.add(SymptomsParameterResult.objects.create(parameter=parameter, value=value))
                return redirect(reverse('clinical_view')+'/'+str(clinical.id)+'/symptoms')
            error_message = _("You should enter any of the parameters")
  
    fields = SymptomsParameterTranslate.objects.all().values_list('name', flat=True)
    return render_to_response('symptoms.html',{
                                                   'nav_symptoms' : True,
                                                   'title': _('Symptoms'),
                                                   'verbose_model' : Symptoms._meta.verbose_name,
                                                   'module_name' : Symptoms._meta.verbose_name,
                                                   'data' : get_values(fields, SymptomsParameterTranslate),
                                                   'clinical': clinical,
                                                   'error_message' : error_message,
                                                   },
                                                   context_instance=RequestContext(request))    
@login_required    
def analisys(request, type=None, id=None):
    """ Analisys view """
    error_message = None
    clinical = None
    
    if id:
        clinical = Clinical.objects.get(id=id)
    else:
        clinical = Clinical.objects.get(id=request.POST['clinical_id'])
    
    if request.method == 'POST':
        if not 'history_number' in request.POST:
            data = clean_dict(request.POST)
            if len(data) > 0:
                analisys = Analisys.objects.create(created = datetime.now(), alias=request.POST.get('alias', ''))
                clinical.analisys.add(analisys)
                for element in data:
                    if element != 'alias':
                        parameter = AnalisysParameterTranslation.objects.get(name=element).model
                        for i in range(1,len(data[element])):
                            value = ParameterValuesTranslation.objects.get(value = data[element][i]).model
                            analisys.parameter_result.add(AnalisysParameterResult.objects.create(parameter=parameter, value=value))
                #TODO: fix generate_report
                generate_report(clinical)
                
                return redirect(reverse('clinical_view')+'/'+str(clinical.id)+'/analisys')
            error_message = _("You should enter any of the parameters")    

    
    if type == 'avanced':
        fields = AnalisysParameterTranslation.objects.filter(model__is_basic=False).values_list('name', flat=True)
    else:
        type = 'basic'
        fields = AnalisysParameterTranslation.objects.filter(model__is_basic=True).values_list('name', flat=True)
        
    return render_to_response('analisys.html',{
                                                   'nav_analisys' : True,
                                                   'title': _('Analisys'),
                                                   'verbose_model' : Analisys._meta.verbose_name,
                                                   'module_name' : Analisys._meta.verbose_name,
                                                   'data' : get_values(fields, AnalisysParameterTranslation),
                                                   'clinical' : clinical,
                                                   'error_message' : error_message,
                                                   'analisys_type': type,                                                   
                                                   },
                                                   context_instance=RequestContext(request))


@login_required    
def validate(request, id=None):
    """ Validate or invalidate a Clinical by an admin """
    if id:
        clinical = Clinical.objects.get(id=id)
        if clinical.valid_to_study:
            clinical.valid_to_study = False
        else:
            clinical.valid_to_study = True
        clinical.save()
    return redirect(reverse('clinical_view'))
    
    
@login_required
def delete(request, model=None, id=None, clinical_id=None):
    """ Delete an analisys or symptoms """
    object = None
    if id:
        if model == 'analisys':
            object = Analisys.objects.get(id = id)
            message = _('Analisys deleted sucessfully.')
        elif model == 'symptoms':
            object = Symptoms.objects.get(id = id)
            message = _('Symptoms deleted sucessfully.')
        object.delete()
        if clinical_id:
            clinical = Clinical.objects.get(id=clinical_id)
        else:
            clinical = Clinical.objects.get(id=request.POST['clinical_id'])
        generate_report(clinical)
        request.session['message'] = message
    m2m_fields = Clinical._meta.many_to_many
    nav_field_active = m2m_fields[1].name
    return render_to_response('thumb-view.html',{
                                         'nav_clinical' : True, 
                                         'nav_field_active': nav_field_active,
                                         'title' : _('Clinical'),
                                         'm2m_fields': m2m_fields,
                                         'verbose_model' : Clinical._meta.verbose_name,
                                         'module_name' : Clinical._meta.module_name,
                                         'data_object' : get_data_object(clinical, {'fields': ['id','history_number'], 'm2m': [nav_field_active]}),
                                         'new' : False,
                                         'profile': get_profile_name(request.user),
                                         'message': message,
                                         },
                                        context_instance=RequestContext(request))
    #return redirect('/econmet/clinical/'+str(clinical_id))

@login_required
def report_alias(request, clinical_id=None):
    """ Set the alias of the last report generated """
    object = None
    if clinical_id and request.POST:
        report = Clinical.objects.get(id=clinical_id).report.latest('created')
        report.alias = request.POST.get('alias', '')
        report.save() 
    return redirect('/econmet/clinical/'+str(clinical_id)+'/report')
    
    
@login_required
def diagnose(request, id=None):
    """ Diagnose view """
    error_message = None
    clinical = None
    name = None
    type = None
    group = None
    rate_percent = None

    if id:
        clinical = Clinical.objects.get(id=id)
    else:
        clinical = Clinical.objects.get(id=request.POST['clinical_id'])
    
    if request.method == 'POST':
        if not 'history_number' in request.POST:
            data = clean_dict(request.POST)
            es = Language.objects.get(code=request.META['LANG'][:2])
            rate_percent = request.POST.get('rate_percent', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)
            group = request.POST.get('group', None)
            try:
                illness = Illness.objects.create(rate_percent=rate_percent)
                IllnessTranslation.objects.create(language=es, model=illness, name=name, type=type, group=group)
                clinical.illness.add(illness)
                return redirect(reverse('clinical_view')+'/'+str(clinical.id)+'/illness')
            except:
                error_message = _("The rate_percent must be a number")

    fields = [{'name': 'name', 'verbose_name': _('Name'), 'value': name}, 
              {'name': 'type', 'verbose_name': _('Type'), 'value': type},
              {'name': 'group', 'verbose_name': _('Group'), 'value': group},
              {'name': 'rate_percent', 'verbose_name': _('Rate Percent'), 'value': rate_percent}]
        
    return render_to_response('diagnose.html',{
                                                   'nav_analisys' : True,
                                                   'title': _('Illness'),
                                                   'verbose_model' : Illness._meta.verbose_name,
                                                   'module_name' : Illness._meta.verbose_name,
                                                   'data' : fields,
                                                   'clinical' : clinical,
                                                   'error_message' : error_message,                                                   
                                                   },
                                                   context_instance=RequestContext(request)) 
    