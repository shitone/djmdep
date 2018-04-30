from django.urls import path
from cimiss import ws

websocket_urlpatterns = [
    path('ws/awspqc', ws.MyConsumer),
]