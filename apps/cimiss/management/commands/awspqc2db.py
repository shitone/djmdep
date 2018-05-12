from django.core.management.base import BaseCommand
from django.db import transaction
import datetime
from apps.cimiss.models import AwsArrival, AwsSource
from kombu import Connection, Queue
import urllib
import json
from config.basic import Basic


class Command(BaseCommand):

    def handle(self, *args, **options):
        record_queue = Queue('awspqc_record')

        def _record_aws(body, message):
            message.ack()
            timestamp = float(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp).utcnow()
            aws = body['aws']
            inter = body['inter']
            nocenter = body['nocenter']
            intercenter = body['intercenter']

            with transaction.atomic():
                for aw in aws:
                    init_dict = dict()
                    init_dict['data_day'] = now.date()
                    init_dict['station_number'] = aw
                    init_dict['a' + now.strftime('%H')] = 1
                    if aw not in inter:
                        init_dict['p' + now.strftime('%H')] = 1
                    awsarrival = AwsArrival()
                    awsarrival.init_from_dict(init_dict)
                    awsarrival.save()

            f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
            data = json.loads(f.read())
            ass = AwsSource.objects.all()
            with transaction.atomic():
                for a in ass:
                    if a.station_number in data:
                        if a.station_number in nocenter:
                            a.no_center = 1
                        elif a.station_number in intercenter:
                            a.no_center = 3
                        elif a.station_number not in aws:
                            a.no_center = 2
                        else:
                            a.no_center = 0
                        a.save()
                        del data[a.station_number]
                    else:
                        a.delete()
                for key, sinfo in data.items():
                    no = 0
                    if sinfo["stationnum"] in nocenter:
                        no = 1
                    a = AwsSource(station_number=sinfo["stationnum"], no_center=no)
                    a.save()

        with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
            with conn.Consumer(record_queue, accept=['json'], callbacks=[_record_aws]) as consumer:
                while True:
                    try:
                        conn.drain_events()
                    except Exception as e:
                        raise