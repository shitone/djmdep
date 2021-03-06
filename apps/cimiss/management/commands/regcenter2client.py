from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from apps.cimiss.models import AwsArrival, AwsBatteryThreshold
from kombu import Connection, Queue
import urllib
import json
import datetime
import copy


class Command(BaseCommand):

    def handle(self, *args, **options):
        regaws_queue = Queue('regaws')

        def _process_regaws(body, message):
            message.ack()
            f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
            data = json.loads(f.read())
            timestamp = float(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp).utcnow()
            carrival = body['isarr']
            battery = body['battery']
            q = Q()
            q.connector = 'AND'
            q.children.append(('data_day', now.date()))
            q.children.append(('a' + now.strftime('%H'), 1))
            aas = AwsArrival.objects.filter(q)
            aanolist = []
            for aa in aas:
                aanolist.append(aa.station_number)
            srecieves = []
            btrs = []
            thresholds = AwsBatteryThreshold.objects.all()
            bat_thresh = {}
            for bat in thresholds:
                bat_thresh[bat.station_number] = bat.battery_threshold
            for key, sinfo in data.items():
                srecieve = {}
                srecieve["sno"] = sinfo["stationnum"]
                srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
                srecieve["sname"] = sinfo["stationname"]
                srecieve["lon"] = sinfo["lontiude"]
                srecieve["lat"] = sinfo["lattiude"]
                srecieve["county"] = sinfo["county"]
                srecieve["machine"] = sinfo["machine"]
                btr = copy.deepcopy(srecieve)
                srecieve["center_arrival"] = 0
                srecieve["cts_arrival"] = 0
                if sinfo["stationnum"] in carrival:
                    srecieve["center_arrival"] = 1
                if sinfo["stationnum"] in aanolist:
                    srecieve["cts_arrival"] = 1
                srecieves.append(srecieve)
                if sinfo["stationnum"] in battery:
                    btr["battery_value"] = battery[sinfo["stationnum"]]
                else:
                    btr["battery_value"] = -1
                if sinfo["stationnum"] in bat_thresh:
                    btr["thresholds"] = bat_thresh[sinfo["stationnum"]]
                else:
                    btr["thresholds"] = 0
                btrs.append(btr)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'reg_center',
                {
                    'type': 'send2client',
                    'message': json.dumps(srecieves)
                }
            )
            async_to_sync(channel_layer.group_send)(
                'aws_battery',
                {
                    'type': 'send2client',
                    'message': json.dumps(btrs)
                }
            )

        with Connection(settings.TASK_RMQ + '/cimiss') as conn:
            with conn.Consumer(regaws_queue, accept=['json'], callbacks=[_process_regaws], prefetch_count=1) as consumer:
                while True:
                    try:
                        conn.drain_events()
                    except Exception as e:
                        print(e.message)
