from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models     import Departments, People
from .forms      import ViewPeopleForm, LoginForm 
from django.http import Http404
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  
from django.core import serializers
from django.http import HttpResponse
from generator import *
from django.http import Http404
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')    # Do something for authenticated users.
    else:
        return redirect('/myapp/login/') # Redirect to a login page. # Do something for anonymous users.
    
    

def loginn(request):
    if request.method == "POST": # результат запроса
        form = LoginForm(request.POST) 
        if form.is_valid(): # если проверка на валидность прошла успешно:          
            username = form.cleaned_data['user']
            password = form.cleaned_data['passwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)   # привязать к сессии авторизованного пользователя               
                    return redirect('/myapp/') # Redirect to a success page.
                else:
                    return HttpResponse( 'Disabled account!' ) # Return a 'disabled account' error message
            else:
                # Return an 'invalid login' error message.
                return HttpResponse( '<p>Неправильный логин или пароль.</p>  <a href="/myapp/login/">Назад</a>' )
    else:   # страница открывается впервые 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
 


def logout_view(request):
    logout(request)
    return redirect('/myapp/login/') # Redirect to a login page.



def people_list(request):
    if request.user.is_authenticated:             
        department  = request.GET.get('departments')
        check       = request.GET.get('check')
        page        = request.GET.get('page',1)   # number of page, 1 - start value
        queryset = Departments.objects.values_list("Department_name", flat=True) 
        form = ViewPeopleForm(queryset)                    
        PeopleFieldsList = People._meta.get_fields()[1:10]  #список полей модели для шапки таблицы, исключая 'id' и 'department'
        Objects = People.objects.all()   
        # фильтрация    
        if department: 
            Objects = People.objects.filter(department__Department_name = department)
        if check:
            Objects = Objects.filter(end_date = None) # только работающие
        else:                    
            Objects = Objects.all()  # все
        # пагинация              
        paginator = Paginator(Objects, 10)  # 10 записей на страницу  
        Objects = paginator.get_page(page)
        context = { 'PeopleInfo': Objects, 'PeopleFieldsList': PeopleFieldsList, 'form': form, 'page': page, }   
        return render(request, 'people_list.html', context)
    else:
        return redirect('/myapp/login/') # Redirect to a login page. # Do something for anonymous users.
    


def man(request, id):     
    if request.user.is_authenticated:
        try:
            info = People.objects.get(id = id)
        except People.DoesNotExist:
            raise Http404("Сотрудник не найден")
        return render(request, 'man.html', {'info': info}, )
    else:
        return redirect('/myapp/login/') # Redirect to a login page.



def alphabet(request):     
    if request.user.is_authenticated:            
        PeopleTotal = People.objects.all().count() #Всего сотрудников: 
        if PeopleTotal > 6: #Количество групп
            Groups = 7
        else:
            Groups = PeopleTotal              
        GroupLength = PeopleTotal // Groups  #Сотрудников в группе = кол-во сотрудников / 7   
        SortedPeople = People.objects.all() # Все сотрудники, отсортированные по фамилии
        # Прохожусь по всем и раскидываю их на 7 групп
        indexes = [] # границы групп (начальный - конечный индексы)
        a = 0
        b = 0
        counter = 1
        for i in range(PeopleTotal-1): # проход по сотрудникам
            if counter >= GroupLength and SortedPeople[i].SurnameFirstLetter() != SortedPeople[i+1].SurnameFirstLetter():
                b = i
                indexes.append( [a, b] )
                a = i+1
                counter = 0
            counter = counter+1
        #В последнюю группу нужно добавить остатки сотрудников:
        indexes.append( [b+1, PeopleTotal-1] ) #(последний сотрудник из предыдущей группы + 1 , номер самого последнего сотрудника)
        #indexes.append( [indexes[len(indexes)-1][1]+1, PeopleTotal-1] ) #(последний сотрудник из предыдущей группы + 1 , номер самого последнего сотрудника)
        #Прохожусь по каждой группе: 
        #беру первого и последнего сотрудника для определения начальной и конечной буквы интервала, 
        #записываю эти буквы в соответствующие каждой группе множества
        Letters = []
        for j in range(len(indexes)):
            Letters.append([ SortedPeople[indexes[j][0]].SurnameFirstLetter(), SortedPeople[indexes[j][1]].SurnameFirstLetter() ])
        context = { 'Letters': Letters, } 
        
        if 'range' in request.GET: # выбранная группа
            SelectedRange = int(request.GET['range']) -1
            
            Objects = []
            for i in range(PeopleTotal-1): # проход по сотрудникам
                if i in range( indexes[SelectedRange][0], indexes[SelectedRange][1] ):
                    Objects.append(SortedPeople[i]) 
            context = { 'Letters': Letters, 'PeopleInfo': Objects, }   

        return render(request, 'alphabet.html', context)
    else:
        return redirect('/myapp/login/') # Redirect to a login page.



def geberate_records(request):
    if request.user.is_authenticated:            
        if People.objects.all().count() < 300: #если база данных ещё не заполнялась
            Generate() #заполнить
            return HttpResponse( '<p>База данных заполнена.</p>  <a href="/myapp/">Назад</a>' )
        return HttpResponse( '<p>Заполнение не требуется, база данных уже заполнена.</p>  <a href="/myapp/">Назад</a>' )        
    else:
        return redirect('/myapp/login/') # Redirect to a login page.


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="500.html"):
    response = render(template_name)
    response.status_code = 500
    return response
