# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django.shortcuts import render, get_object_or_404
from cms.models import Page, Menu, Language, Configuration, Questionary, FixedValue
from cms.forms import ContactForm
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.mail.message import EmailMessage
from django.core import mail
import os


def _get_theme_selected():
    """
    Gets the selected theme from Configuration model.

    """

    try:
        theme_selected = Configuration.objects.filter(group='theme', key='selected')[0]
        theme_name = theme_selected.value
    except:
        theme_name = 'default'

    return theme_name


def error_404(request):
    """
    404 page
    """

    return render(request, '404.html', {'title': '404 error',})


def error_500(request):
    """
    500 page

    """

    return render(request, '500.html', {'title': '500 error',})   


def home(request):
    """
    Shows the home page for the cms.

    """

    MAX_WIDTH_IMG = 350
    MAX_HEIGHT_IMG = 350
    MAX_WIDTH_CONTENT = 950

    menu = Menu.objects.get(nav_option = "home")
    page = menu.page

    try:
        img_width = page.image.width + 30
        img_height = page.image.height
        difference = 20
        if img_width > MAX_WIDTH_IMG:
            img_width = MAX_WIDTH_IMG
            difference = 50
        data_width = MAX_WIDTH_CONTENT - img_width - difference
    except:
        img_width = None
        data_width = None
        img_height = None

    template_name = os.path.join(_get_theme_selected(), 'home.html')

    return render(request, template_name, {
        'NAV': menu.nav_option,
        'img': page.image,
        'img_width': img_width,
        'img_height': img_height,
        'data_width': data_width,
        'page': page,
        'menu': list(Menu.objects.filter(parent_menu=None).filter(page__active=True)),
        'language': list(Language.objects.all()),
        #'next' : get_next_to_active(list(Menu.objects.filter(parent_menu=None)), menu.nav_option),
    })


def page(request, path):
    """
    Shows a page.
    This view is used to show every pages created with the Page Model.
    All of them use the same template page.html

    """

    MAX_WIDTH_IMG = 350
    MAX_HEIGHT_IMG = 350
    MAX_WIDTH_CONTENT = 950
    
    menu = get_object_or_404(Menu, nav_option = path)
    page = menu.page
         
    subnav = None
    link = None
    
    if not menu.show_owner_page:
        try:
            menu = list(Menu.objects.filter(parent_menu=menu))[0]
        except:
            pass
       
    if menu.parent_menu:
        subnav = menu.nav_option
        menu = menu.parent_menu
    
    submenu = list(Menu.objects.filter(parent_menu=menu))
    if submenu:
        MAX_WIDTH_CONTENT = 740
    
    try:
        img_width = page.image.width + 30
        img_height = page.image.height
        difference = 20
        if img_width > MAX_WIDTH_IMG:
            img_width = MAX_WIDTH_IMG
            difference = 50
        data_width = MAX_WIDTH_CONTENT - img_width - difference
    except:
        img_width = None
        data_width = None
        img_height = None

    template_name = os.path.join(_get_theme_selected(), 'page.html')

    return render(request, template_name, {
        'NAV' : menu.nav_option,
        'SUBNAV' : subnav,
        'img' : page.image,
        'img_width' : img_width,
        'img_height' : img_height,
        'data_width' : data_width,
        'page' : page,
        'menu' : list(Menu.objects.filter(parent_menu=None)),
        'submenu' : submenu,
        'language' : list(Language.objects.all()),
        'title' : menu.name,
        'link' : link,
        'next' : get_next_to_active(list(Menu.objects.filter(parent_menu=None)), menu.nav_option),
        'contact_label' : FixedValue.objects.get(key="contact").value,
    })


def contact(request):
   
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
        
            mail = Configuration.objects.get(key="mail")
            recipients = [mail.value]
            if cc_myself:
                recipients.append(sender)
        
            connection=getConnectionData()
            EmailMessage(subject, message, sender, recipients,
                        connection=connection).send()
            return HttpResponseRedirect('/home/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
        
    try:
        lang = request.COOKIES['language']
    except:
        lang = request.META['HTTP_ACCEPT_LANGUAGE'].split('-')[0]        
    
    template_name = os.path.join(_get_theme_selected(), 'contact.html')

    return render(request, template_name, {
        'form': form,
        'NAV' : None,
        'page' : None,
        'menu' : list(Menu.objects.filter(parent_menu=None)),
        'submenu' : None,
        'language' : list(Language.objects.all()),
        'title' : _(u'Contacto')
    })
 
def get_next_to_active(menu, nav_option):
    counter = 0
    for item in menu:
        if item.nav_option == nav_option:
            return counter + 1
        counter +=1
    return 0
            
####################################################################################################
# The methods below must be extracted to a plug-in
####################################################################################################
def partnership(request):

    page = Page.objects.get(url="partnership")
    
    try:
        lang = request.COOKIES['language']
    except:
        lang = request.META['HTTP_ACCEPT_LANGUAGE'].split('-')[0]    
    
    template_name = os.path.join(_get_theme_selected(), 'page.html') # was selected home.html ¿?

    return render(request, template_name, {
        'NAV' : None,
        'LANG' : lang,
        'page' : page,
        'menu' : list(Menu.objects.filter(parent_menu=None)),
        'submenu' : None,
        'language' : list(Language.objects.all()),
        'title' : _(u'Partnership'),
        'contact_label' : FixedValue.objects.get(key="contact").value,
        'partnership_label': FixedValue.objects.get(key="partnership").value,
        'print_label': FixedValue.objects.get(key="print").value,
    })
    
# TODO: Fix it!! 
def getConnectionData():
       
    connection = mail.get_connection()
    connection.username=Configuration.objects.get(key="server_user").value
    connection.password=Configuration.objects.get(key="server_pass").value
    connection.host=Configuration.objects.get(key="server_host").value
    connection.port=int(Configuration.objects.get(key="server_port").value)
    connection.use_tls=Configuration.objects.get(key="server_tls").value
    
    return connection   

def questionary(request):
    questionary = Questionary.objects.get(alias='Questionary')
    template = ''
    
    if request.method == 'POST': # If the form has been submitted...
        mail = Configuration.objects.get(key="mail")
        
        match_question = match_questions_results(questionary, request.POST)
        match_parameter = match_parameters_results(questionary, request.POST)
        match_extra_parameter = match_extra_parameters_results(request.POST)
        template = questionary_template(questionary, match_question, match_parameter, match_extra_parameter)
        
        connection=getConnectionData()
        subject = "Cuestionario"
        sender = "Cuestionario"
        recipients = [mail.value]
        message = template
        msg = EmailMessage(subject, message, sender, recipients,connection=connection)
        msg.content_subtype = "html"  # Main content is now text/html 
        #msg.send()
        #return HttpResponseRedirect('/home/') # Redirect after POST        

    try:
        lang = request.COOKIES['language']
    except:
        lang = request.META['HTTP_ACCEPT_LANGUAGE'].split('-')[0]
    
    template_name = os.path.join(_get_theme_selected(), 'questionary.html')

    return render(request, template_name, {
        'NAV' : None,
        'LANG' : lang,
        'questionary' : questionary,
        'questions' : list(questionary.questions.all()),
        'menu' : list(Menu.objects.filter(parent_menu=None)),
        'submenu' : None,
        'language' : list(Language.objects.all()),
        'title' : _(u'Cuestionario'),
        'resu' : template,
        'contact_label' : FixedValue.objects.get(key="contact").value,
        'partnership_label': FixedValue.objects.get(key="partnership").value,
        'print_label': FixedValue.objects.get(key="print").value,
        'is_required' : FixedValue.objects.get(key="required").value,
        'parameter_label' : FixedValue.objects.get(key="parameter").value,
        'minimum_label': FixedValue.objects.get(key="minimum").value,
        'maximum_label': FixedValue.objects.get(key="maximum").value,
        'pic_label': FixedValue.objects.get(key="pic").value,
        'unit_label': FixedValue.objects.get(key="unit").value,
        'parameter_required' : FixedValue.objects.get(key="parameter_required").value,
        'send_label' : FixedValue.objects.get(key="send").value,
    }) 
    
# TODO: move this methods another file
def match_questions_results(questionary, post):
    kwargs = []
    for question in list(questionary.questions.all()):
        c_questions = list(question.complex_question.all()) 
        if c_questions.__len__() > 1:
            c_value = []
            for c_question in c_questions:
                name = question.question+'_'+c_question.question
                value = post.getlist(name)[0]
                if value != '':
                    c_value.append(c_question.question+': '+value)
            kwargs.append((question.question, c_value))
        else:
            name = question.question
            value = post.getlist(name)
            try:
                kwargs.append((name,value))
            except:
                pass
    return kwargs

def match_parameters_results(questionary, post):
    kwargs = []
    for parameter in list(questionary.parameters.all()):
        param = []
        empty = True
        for x in ['_min','_max','_pic']:
            value = post.getlist(parameter.parameter+x)[0]
            param.append(value)
            if value != '':
                empty = False
        if not empty:
            kwargs.append((parameter.parameter, param, parameter.unit))
    return kwargs
    
def match_extra_parameters_results(post):
    kwargs = []
    for x in range(4):
        name_parameter = post.getlist('parametro_extra1')[x]
        if name_parameter != '':
            param = []
            empty = True
            for y in ['minimo_', 'maximo_', 'pico_']:
                value = post.getlist(y+'extra1')[x]
                param.append(value)
                if value != '':
                    empty = False
            if not empty:
                kwargs.append((name_parameter, param, post.getlist('unidad_extra1')[x])) 
    return kwargs

# TODO: fix this, what is this??
def questionary_template(questionary, questions, parameters, extra_parameters):
    questionary_template = """
    <div id='questionary'>
        <h1 align = center>{{questionary.name}}</h1>
        <br>
        <div id='questionary_form'>
            <ol>
            {% for name, values in questions %}
                <li>
                    <strong>{{name}}:</strong> 
                    {% if values|length == 1 %}
                        {{values.0}}
                    {% else %}
                        <ul>
                        {% for value in values %}
                            <li>{{value}}</li>
                        {% endfor %}
                        </ul>
                    {% endif %} 
                </li>
            {% endfor %}
            </ol>
            {% if parameters or extra_parameters %}
                <table>
                    <tbody>
                        <tr>
                            <th style='width:338px'>Parámetro</th><th style='width:113px'>Mínimo</th><th style='width:113px'>Máximo</th><th style='width:113px'>Pico</th><th style='width:113px'>Unidad</th>
                        </tr>
                        {% for name, values, unit in parameters %}
                            <tr style='border: 1px solid black;'>
                                <td align='left' style='border: 1px solid black;'>{{name}}</td>
                                {% for value in values %}
                                    <td align='center' style='border: 1px solid black;'>{{value}}</td>
                                {% endfor %}
                                <td style='border: 1px solid black;'>{{unit}}</td>
                            </tr>
                        {% endfor %}
                        {% for name, values, unit in extra_parameters %}
                            <tr style='border: 1px solid black;'>
                                <td align='left' style='border: 1px solid black;'>{{name}}</td>
                                {% for value in values %}
                                    <td align='center' style='border: 1px solid black;'>{{value}}</td>
                                {% endfor %}
                                <td style='border: 1px solid black;'>{{unit}}</td>
                            </tr>
                        {% endfor %}                  
                    </tbody>
                </table>
            {% endif %}            
        </div>
    </div>    
    """
    from django.template import Template, Context
    t = Template(questionary_template)
    c = Context({
                 'questionary' : questionary,
                 'questions' : questions,
                 'parameters' : parameters,
                 'extra_parameters' : extra_parameters,
                 })
    return t.render(c)
  
