from django.urls import path
from apps.main import views

app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name=''),
    path('dashboard', views.dashboard, name='dashboard'),
]