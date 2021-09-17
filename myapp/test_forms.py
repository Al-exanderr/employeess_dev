from django.test import TestCase
from .forms import *

class LoginFormTest(TestCase):
    # проверка текстовых меток на соответствие
    def test_LoginForm_user_label(self):
        self.assertTrue( LoginForm().fields['user'].label == 'Логин' )

    def test_LoginForm_passwd_label(self):
        self.assertTrue( LoginForm().fields['passwd'].label == 'Пароль' )


class ViewPeopleFormFormTest(TestCase):
    def test_ViewPeopleForm_departments_label(self):
        self.assertTrue( ViewPeopleForm().fields['departments'].label == 'Отдел:' )