from django.test import TestCase
from .models import *
from generator import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse



class People_list_view_test(TestCase):

    def setUp(self):
        # Создание пользователя, отдела и 12-ти апостолов)
        User.objects.create_user(username='admin', password='0123456789').save()
        Departments.objects.create(Department_name = 'Отдел сбыта')
        Departments.objects.create(Department_name = 'Служба безопастности')
        #Departments.objects.create(Department_name = 'Отдел закупок')
        for num in range(12):
            People.objects.create(
                surname         = 'Фамилия № %s' % num,
                name            = 'Имя № %s' % num,
                patronymic      = 'Отчество № %s' % num,
                birth_date      = '1990-06-06',
                email           = 'e_mail %s @gmail.com' % num,
                start_date      = '2020-03-03',          
                position        = 'Профессия № %s' % num,
                department_id   = 1 )

    # проверка редиректа, когда пользователь не залогинился                
    def test_redirect_from_people_list_page_if_not_logged_in(self):
        resp = self.client.get(reverse('people_list'))
        self.assertRedirects(resp, '/myapp/login/')

    def test_redirect_from_index_page_if_not_logged_in(self):
        resp = self.client.get(reverse('index'))
        self.assertRedirects(resp, '/myapp/login/')

    def test_redirect_from_man_page_if_not_logged_in(self):
        resp = self.client.get('/myapp/man/1/')
        self.assertRedirects(resp, '/myapp/login/')

    def test_redirect_from_alphabet_page_if_not_logged_in(self):
        resp = self.client.get(reverse('alphabet'))
        self.assertRedirects(resp, '/myapp/login/')

    def test_redirect_from_geberate_records_page_if_not_logged_in(self):
        resp = self.client.get(reverse('geberate_records'))
        self.assertRedirects(resp, '/myapp/login/')

    def test_logged_in(self):
        login = self.client.login(username='admin', password='0123456789')
        #проверка возможности залогииться
        resp = self.client.get(reverse('loginn'))   
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'admin')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    # Проверка на то, что некорректный опльзователь не смог залогинилься

    # Проверка доступности всех ссылок после того, как пользователь залогинился
    def test_view_login_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='0123456789')
        resp = self.client.get('/myapp/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/myapp/geberate_records/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/myapp/people_list/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/myapp/alphabet/')
        self.assertEqual(resp.status_code, 200)        
        resp = self.client.get('/myapp/man/1/')
        self.assertEqual(resp.status_code, 200)    
        resp = self.client.get('/myapp/logout/')
        self.assertEqual(resp.status_code, 302) # 302, потому что происходит редирект на /myapp/login/       

    # Проверка пагинации (показывается 10 экземпляров на страницу из 12)
    def test_pagination_after_login_in(self):
        login = self.client.login(username='admin', password='0123456789')
        resp = self.client.get(reverse('people_list'))
        self.assertEqual( len(resp.context['PeopleInfo']), 10 )
    
    # Проверка правильности используемых шаблонов 
    def test_correct_templates(self):
        login = self.client.login(username='admin', password='0123456789')
        #----
        resp = self.client.get(reverse('loginn'))                   
        self.assertTemplateUsed(resp, 'login.html')
        #----
        resp = self.client.get(reverse('index'))                   
        self.assertTemplateUsed(resp, 'index.html')
        #----
        resp = self.client.get(reverse('people_list'))                   
        self.assertTemplateUsed(resp, 'people_list.html')
        #----
        resp = self.client.get('/myapp/man/1/')                   
        self.assertTemplateUsed(resp, 'man.html')
        #----
        resp = self.client.get(reverse('alphabet'))   
        self.assertTemplateUsed(resp, 'alphabet.html')


    # Содержатся ли запросы пагинации и фильтрации в запросе к people_list
    # Реакция на фильрацию и пагинацию
 
class PeopleInstancesViewTest(TestCase):

    def setUp(self):     
        # Создание двух пользователей, двух отделов и 12-ти сотрудников
        test_user1 = User.objects.create_user(username='superadmin', password='0123456789')
        test_user1.save()
        Departments.objects.create(Department_name = 'Отдел сбыта')
        Departments.objects.create(Department_name = 'Служба безопастности')
        for num in range(12):
            People.objects.create(
                surname         = 'Фамилия № %s' % num,
                name            = 'Имя № %s' % num,
                patronymic      = 'Отчество № %s' % num,
                birth_date      = '1990-06-06',
                email           = 'e_mail %s @gmail.com' % num,
                start_date      = '2020-03-03',          
                position        = 'Профессия № %s' % num,
                department_id   = 1 )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('people_list') )
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/myapp/login/') )


    def test_redirect_if_logged_in_but_not_correct(self):
        login = self.client.login(username='testuser1', password='001122')
        resp = self.client.get(reverse('people_list') )

        # Проверка условия: редирект на /myapp/login/, если пользователь не авторизован
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/myapp/login/') )
    
        # Если пользователь авторизован, редирект не происходит
    def test_logged_in_with_correct_user(self):
        login = self.client.login(username='superadmin', password='0123456789')
        resp = self.client.get(reverse('people_list') )
        self.assertEqual( resp.status_code,200)

    # если некорректный id сотрудника, должен возвращаться код 404:
    def test_HTTP404_for_invalid_man_id(self):        
        login = self.client.login(username='superadmin', password='0123456789')
        resp = self.client.get('/myapp/man/99999/')
        self.assertEqual( resp.status_code,404)
        # ну и заодно проверяю шаблон
        self.assertTemplateUsed(resp, '404.html')
    

class OtherTests(TestCase):

    def setUp(self):     
        # Создаю пользователя и 3 отдела. Работников пока нет.
        test_user = User.objects.create_user(username='admin', password='012345')
        test_user.save()

    # проверка генератора для начального заполнения БД
    def test_records_initial_creation(self):        
        Generate()
        number_of_records_created = People.objects.all().count()
        last_department = Departments.objects.all()[4].Department_name
        self.assertEqual( number_of_records_created, 400 )
        self.assertEqual( last_department, 'Секретариат' )

    # Прхоже этих тестов можно придумать очень много,
    # думаю для тестового задания достаточно )