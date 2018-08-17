from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from kombu import Connection, Queue
import urllib
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        awspqc_queue = Queue('awspqc')

        def _process_aws(body, message):
            message.ack()
            f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
            data = json.loads(f.read())
            timestamp = body['timestamp']
            aws = body['aws']
            inter = body['inter']
            nocenter = body['nocenter']
            intercenter = body['intercenter']
            srecieves = []
            for key, sinfo in data.items():
                srecieve = {}
                srecieve["sno"] = sinfo["stationnum"]
                srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
                srecieve["sname"] = sinfo["stationname"]
                srecieve["lon"] = sinfo["lontiude"]
                srecieve["lat"] = sinfo["lattiude"]
                srecieve["original"] = 0
                srecieve["county"] = sinfo["county"]
                srecieve["machine"] = sinfo["machine"]
                srecieve["pqc"] = 0
                if sinfo["stationnum"] in aws:
                    srecieve["original"] = 1
                    if sinfo["stationnum"] not in inter:
                        srecieve["pqc"] = 1
                if sinfo["stationnum"] in nocenter:
                    srecieve["nocenter"] = 1
                elif sinfo["stationnum"] in intercenter:
                    srecieve["nocenter"] = 3
                elif srecieve["original"] == 1:
                    srecieve["nocenter"] = 0
                else:
                    srecieve["nocenter"] = 2
                srecieves.append(srecieve)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'aws_info',
                {
                    'type': 'send2client',
                    'message': json.dumps(srecieves)
                }
            )

        with Connection(settings.TASK_RMQ + '/cimiss') as conn:
            with conn.Consumer(awspqc_queue, accept=['json'], callbacks=[_process_aws], prefetch_count=1) as consumer:
                while True:
                    try:
                        conn.drain_events()
                    except Exception as e:
                        print(e.message)
