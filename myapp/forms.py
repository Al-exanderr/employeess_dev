 

from typing import ValuesView
from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, CharField, TextInput
from django.core.exceptions import ValidationError
from django.forms.fields import ChoiceField
from django.forms.models import fields_for_model
from django.utils.translation import ugettext_lazy as _
from .models import *


class LoginForm(forms.Form):
    user   = CharField( max_length=20, label='Логин')
    passwd = CharField( max_length=20, label='Пароль', widget=forms.PasswordInput)


class ViewPeopleForm(forms.Form):
    queryset = Departments.objects.values_list("Department_name", flat=True) 
    departments = forms.ChoiceField(choices=[(x,x) for x in queryset], label='Отдел:') # initial='Все'
    #check = forms.BooleanField(required=False, label='Только работающие')