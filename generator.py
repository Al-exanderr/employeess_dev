#from genericpath import exists
import pandas as pd
import numpy as np
from django.utils import timezone
from myapp.models import *
import random
from faker import Faker # Использую Facker для начального заполнения БД

Faker.seed(0)
fake = Faker('ru_RU')


def Generate():
  if not Departments.objects.filter(Department_name = 'Отдел кадров').exists():
    Departments( Department_name = 'Отдел кадров').save()
  if not Departments.objects.filter(Department_name = 'Отдел закупок').exists():
    Departments( Department_name = 'Отдел закупок').save()
  if not Departments.objects.filter(Department_name = 'Бухгалтерия').exists():
    Departments( Department_name = 'Бухгалтерия').save()
  if not Departments.objects.filter(Department_name = 'Отдел сбыта').exists():
    Departments( Department_name = 'Отдел сбыта').save()
  if not Departments.objects.filter(Department_name = 'Секретариат').exists():
    Departments( Department_name = 'Секретариат').save()
  for i in range(400):
    p = People( surname         = fake.last_name(),
                name            = fake.first_name(),
                patronymic      = fake.first_name(),
                birth_date      = fake.date(),
                email           = fake.email(),
                phone_number    = fake.phone_number(),
                start_date      = fake.date(),
                end_date        = random.choice([fake.date(),None]),
                position        = fake.job(), 
                department      = Departments.objects.order_by('?').first()
    )
    p.save()
  return 1



