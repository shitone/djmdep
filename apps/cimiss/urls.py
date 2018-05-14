from django.urls import path
from apps.cimiss import views

app_name = 'cimiss'

urlpatterns = [
    path('awsarrival', views.awsarrival, name='awsarrival'),
    path('awsarrivalc', views.awsarrivalc, name='awsarrivalc'),
    path('initaws', views.initaws, name='initaws'),
    path('awsregsource', views.awsarrival, name='awsregsource'),
    path('awsregsourcec', views.awsarrivalc, name='awsregsourcec'),
    path('initawssource', views.initaws, name='initawssource'),
]

# import apps.cimiss.tests