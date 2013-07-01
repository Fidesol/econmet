# -*- coding: utf-8 -*-
__autor__ = "Jose Jiménez Lopez, Fundación I+D del Software Libre"
__email__ = "jjimenez@fidesol.org"
__date__ = "10/05/2012"

from django import forms
from cms.models import FixedValue
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    """
    Form used for the Contact page.

    """

    subject = forms.CharField(max_length=150, 
                              error_messages={'required': _(u'Introduzca el nombre')}, 
                              widget=forms.TextInput(attrs={'size':'45', 'class':'input_text_contact required', 'title': 'Introduzca el nombre'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'44', 'class':'input_text_contact required'}), 
                              error_messages={'required': _(u'Introduzca la consulta a realizar')}, 
                              label=_(u'Consulta'))
    sender = forms.EmailField(error_messages={'required': _(u'Introduzca el correo electronico')}, 
                              label=_(u'Correo Electronico'),
                              widget=forms.TextInput(attrs={'size':'45', 'class':'input_text_contact required'}))
    cc_myself = forms.BooleanField(required=False, 
                                   label=_(u'Desea que le enviemos una copia de su consulta'))
    

                               
