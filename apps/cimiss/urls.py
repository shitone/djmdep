from django.urls import path
from . import views

app_name = 'cimiss'

urlpatterns = [
    path('awsarrival', views.awsarrival, name='awsarrival'),
    path('awsarrivalc', views.awsarrivalc, name='awsarrivalc'),
    path('initaws', views.initaws, name='initaws'),
]