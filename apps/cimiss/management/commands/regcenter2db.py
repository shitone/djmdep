from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
import datetime
from apps.cimiss.models import RegCenterArrival, AwsBattery
from kombu import Connection, Queue
import re


class Command(BaseCommand):

    def handle(self, *args, **options):
        record_queue = Queue('regaws_record')

        def _record_regaws(body, message):
            message.ack()
            timestamp = float(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp).utcnow()
            carrivals = body['isarr']
            batterys = body['battery']
            carrivals_set = set(carrivals)
            with transaction.atomic():
                for rca in RegCenterArrival.objects.filter(data_day=now.date()):
                    init_dict = dict()
                    if rca.station_number in carrivals_set:
                        init_dict['c' + now.strftime('%H')] = 1
                        carrivals_set.remove(rca.station_number)
                    else:
                        init_dict['c' + now.strftime('%H')] = 0
                    rca.init_from_dict(init_dict)
                    rca.save()
                create_objs = []
                for ca in carrivals_set:
                    init_dict = dict()
                    init_dict['data_day'] = now.date()
                    init_dict['station_number'] = ca
                    init_dict['c' + now.strftime('%H')] = 1
                    rcarrival = RegCenterArrival()
                    rcarrival.init_from_dict(init_dict)
                    create_objs.append(rcarrival)
                RegCenterArrival.objects.bulk_create(create_objs)

            with transaction.atomic():
                for ab in AwsBattery.objects.filter(data_day=now.date()):
                    init_dict = dict()
                    if ab.station_number in batterys:
                        battery_value = batterys[ab.station_number]
                        if (battery_value is None) or (not re.match(r'-?\d+(\.\d+)?', battery_value)):
                            init_dict['b' + now.strftime('%H')] = -1.0
                        else:
                            init_dict['b' + now.strftime('%H')] = float(battery_value)
                        batterys.pop(ab.station_number)
                    else:
                        init_dict['b' + now.strftime('%H')] = -1.0
                    ab.init_from_dict(init_dict)
                    ab.save()
                create_objs = []
                for btr in batterys:
                    init_dict = dict()
                    init_dict['data_day'] = now.date()
                    init_dict['station_number'] = btr
                    battery_value = batterys[btr]
                    if (battery_value is None) or (not re.match(r'-?\d+(\.\d+)?', battery_value)):
                        init_dict['b' + now.strftime('%H')] = -1.0
                    else:
                        init_dict['b' + now.strftime('%H')] = float(battery_value)
                    abattery = AwsBattery()
                    abattery.init_from_dict(init_dict)
                    create_objs.append(abattery)
                AwsBattery.objects.bulk_create(create_objs)

        with Connection(settings.TASK_RMQ + '/cimiss') as conn:
            with conn.Consumer(record_queue, accept=['json'], callbacks=[_record_regaws], prefetch_count=1) as consumer:
                while True:
                    try:
                        conn.drain_events()
                    except Exception as e:
                        raise
