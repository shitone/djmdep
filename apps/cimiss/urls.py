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
    path('awshistory', views.awshistory, name='awshistory'),
    path('awshistoryc', views.awshistoryc, name='awshistoryc'),
    path('getawshistory/<str:daystr>', views.getawshistory, name='getawshistory'),
    path('getcenter2cts/<str:hourstr>', views.getcenter2cts, name='getcenter2cts'),
    path('batterythreshold/<str:station>/<str:threshold>', views.batterythreshold, name='batterythreshold'),

]

# import apps.cimiss.tasks