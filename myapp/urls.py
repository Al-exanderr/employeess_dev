from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    # /myapp/
    path('', views.index, name='index'),    

    # /myapp/login/
    path('login/', views.loginn, name='loginn'),   

    # /myapp/logout/
    path('logout/', views.logout_view, name='logout_view'),   

    # /myapp/geberate_records/
    path('geberate_records/', views.geberate_records, name='geberate_records'), 

    # /myapp/people_list/
    path('people_list/', views.people_list, name='people_list'),   

    # /myapp/man/<int:id>/
    path('man/<int:id>/', views.man, name='man'), 

    # /myapp/alphabet/
    path('alphabet/', views.alphabet, name='alphabet'),   
    ]    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
