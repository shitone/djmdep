from django.urls import path
from apps.product import views

app_name = 'product'

urlpatterns = [
    path('surface/tmp', views.tmp, name='tmp'),
    path('surface/tmpc', views.tmpc, name='tmpc'),
    path('surface/wind', views.wind, name='wind'),
    path('surface/windc', views.windc, name='windc'),
]

# import apps.cimiss.tests