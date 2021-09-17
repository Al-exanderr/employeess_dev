from django.test import TestCase
from .models     import Departments, People


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Departments.objects.create(Department_name = 'Отдел сбыта')
        People.objects.create(
            surname         = 'Андреев',
            name            = 'Андрей',
            patronymic      = 'Андреевич',
            birth_date      = '1990-06-27',
            email           = 'andy_andreev@gmail.com',
            #phone_number    = '+79856472214',
            start_date      = '2020-03-19',          
            position        = 'Правовед',
            department_id   = 1
        )
        People.objects.create(  
            surname         = 'Абачкин',
            name            = 'Иван',
            patronymic      = 'Константинович',
            birth_date      = '1991-09-17',
            email           = 'ab.constant@gmail.com',
            start_date      = '2021-01-20',          
            position        = 'Художник',
            department_id   = 1
        )

    # тесты на соответствие текстовых меток полей
    def test_Department_name_label(self):
        departments=Departments.objects.get(id=1)    
        field_label = departments._meta.get_field('Department_name').verbose_name
        self.assertEquals(field_label, 'Oтдел')

    def test_surname_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('surname').verbose_name
        self.assertEquals(field_label, 'Фамилия')
    
    def test_name_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Имя')

    def test_patronymic_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('patronymic').verbose_name
        self.assertEquals(field_label, 'Отчество')

    def test_birth_date_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('birth_date').verbose_name
        self.assertEquals(field_label, 'Дата рождения')
    
    def test_email_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'Эл. почта')

    def test_phone_number_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'Телефон')

    def test_start_date_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('start_date').verbose_name
        self.assertEquals(field_label, 'Дата начала работы')    

    def test_end_date_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('end_date').verbose_name
        self.assertEquals(field_label, 'Дата окончания работы')    

    def test_position_label(self):
        people=People.objects.get(id=1)    
        field_label = people._meta.get_field('position').verbose_name
        self.assertEquals(field_label, 'Должность')


# тесты на соответствие длинны полей    
    def test_Department_name_max_length(self):
        departments=Departments.objects.get(id=1)    
        max_length = departments._meta.get_field('Department_name').max_length
        self.assertEquals(max_length, 50)  

    def test_surname_max_length(self):
        people=People.objects.get(id=1)    
        max_length = people._meta.get_field('surname').max_length
        self.assertEquals(max_length, 30)
    
    def test_name_max_length(self):
        people=People.objects.get(id=1)    
        max_length = people._meta.get_field('name').max_length
        self.assertEquals(max_length, 30)        
    
    def test_patronymic_max_length(self):
        people=People.objects.get(id=1)    
        max_length = people._meta.get_field('patronymic').max_length
        self.assertEquals(max_length, 30)

    def test_position_max_length(self):
        people=People.objects.get(id=1)    
        max_length = people._meta.get_field('position').max_length
        self.assertEquals(max_length, 50)

# тесты на соответствие verbose name    
    def test_Department_verbose_name(self):
        departments=Departments.objects.get(id=1)    
        departments_verbose_name = departments._meta.verbose_name
        self.assertEquals(departments_verbose_name, 'Отдел') 
    
    def test_Department_verbose_name_plural(self):
        departments=Departments.objects.get(id=1)    
        departments_verbose_name_plural = departments._meta.verbose_name_plural
        self.assertEquals(departments_verbose_name_plural, 'Отделы') 
    
    def test_People_verbose_name(self):
        people=People.objects.get(id=1)    
        People_verbose_name = people._meta.verbose_name
        self.assertEquals(People_verbose_name, 'Работник') 
    
    def test_People_verbose_name_plural(self):
        people=People.objects.get(id=1)    
        People_verbose_name_plural = people._meta.verbose_name_plural
        self.assertEquals(People_verbose_name_plural, 'Работники') 


# тесты на соответствие __str__(self)  
    def test_Department_str_(self):
        departments=str(Departments.objects.get(id=1))
        self.assertEquals(departments, 'Отдел сбыта') 

    def test_People_str_(self):
        people=str(People.objects.get(id=1))
        self.assertEquals(people, 'Андреев') 

    def test_People_SurnameFirstLetter(self):
        people=People.objects.get(id=1).SurnameFirstLetter()
        self.assertEquals(people, 'А') 

# тест на сортировку по умолчанию
    def test_People_ordering(self):
        people=People.objects.all()[0].surname
        self.assertEquals(people, 'Абачкин') 
