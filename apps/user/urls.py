from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('department', views.department, name='department'),
    path('iplogin', views.iplogin, name='iplogin'),
    path('logout', views.logout, name='logout'),
]