 

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
    def __init__(self, queryset, *args,**kwargs): # переопределяю __init__ c аргументом queryset, в котором набор всех отделов
        super(ViewPeopleForm,self).__init__(*args,**kwargs) # ниже добавляю поле ChoiceField c отделами
        self.fields['departments']= forms.ChoiceField(choices=tuple([(name, name) for name in queryset]), label='Отдел:')

