from django.core.management.base import BaseCommand, CommandError
import datetime, time
from django.db.models import Q
from apps.cimiss.models import AwsArrival
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("I'm a test job!")
        while True:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'aws',
                {
                    'type': 'chat_m',
                    'message': '666'
                }
            )
            time.sleep(5)
