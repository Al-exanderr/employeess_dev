from django.contrib import admin
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from .models import People, Departments
#from django.utils.translation import ugettext_lazy as _


# Register your models here.

admin.site.register(People)
admin.site.register(Departments)

