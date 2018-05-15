from django.urls import path
from cimiss import ws

websocket_urlpatterns = [
    path('ws/cimiss/awspqc/awsinfo', ws.AWSPQCConsumer),
]
