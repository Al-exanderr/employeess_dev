from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField




class Departments(models.Model):
  Department_name = models.CharField(max_length=50, unique=True, verbose_name='Oтдел')
 
  class Meta:
    verbose_name = 'Отдел'
    verbose_name_plural = 'Отделы'

  def __str__(self):  
    return self.Department_name


class People(models.Model):
  surname         = models.CharField(max_length=30, verbose_name='Фамилия')
  name            = models.CharField(max_length=30, verbose_name='Имя')
  patronymic      = models.CharField(max_length=30, verbose_name='Отчество')
  birth_date      = models.DateField(verbose_name='Дата рождения')
  email           = models.EmailField(verbose_name='Эл. почта') #(max_length=254, **options)
  phone_number    = PhoneNumberField(verbose_name='Телефон')
  #phone_number    = models.CharField(max_length=13, verbose_name='Телефон')
  start_date      = models.DateField(default=None, verbose_name='Дата начала работы')
  end_date        = models.DateField(default=None, blank=True, null=True, verbose_name='Дата окончания работы') #(пустая если всё ещё работает)
  position        = models.CharField(max_length=50, default=None, verbose_name='Должность') # занимаемая должность
  department      = models.ForeignKey(Departments, on_delete=models.CASCADE) #внешн ключ. Связь многие к одному. 

  def __str__(self):  
    return self.surname

  def SurnameFirstLetter(self):
    return self.surname[:1]
  
  class Meta:
    verbose_name = 'Работник'
    verbose_name_plural = 'Работники'
    ordering = ['surname']
