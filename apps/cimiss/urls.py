from django.urls import path
from apps.cimiss import views

app_name = 'cimiss'

urlpatterns = [
    path('awsarrival', views.awsarrival, name='awsarrival'),
    path('awsarrivalc', views.awsarrivalc, name='awsarrivalc'),
    path('initaws', views.initaws, name='initaws'),
    path('awsregsource', views.awsregsource, name='awsregsource'),
    path('awsregsourcec', views.awsregsourcec, name='awsregsourcec'),
    path('initawssource', views.initawssource, name='initawssource'),
    path('regcenter', views.regcenter, name='regcenter'),
    path('regcenterc', views.regcenterc, name='regcenterc'),
    path('initregcenter', views.initregcenter, name='initregcenter'),
    path('awsbattery', views.awsbattery, name='awsbattery'),
    path('awsbatteryc', views.awsbatteryc, name='awsbatteryc'),
    path('initawsbattery', views.initawsbattery, name='initawsbattery'),
]

# import apps.cimiss.tests