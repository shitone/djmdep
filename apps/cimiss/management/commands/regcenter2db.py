from django.core.management.base import BaseCommand
from django.db import transaction
import datetime
from apps.cimiss.models import RegCenterArrival, AwsBattery
from kombu import Connection, Queue
from config.basic import Basic


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
            batterys_set = set(batterys)
            with transaction.atomic():
                for rca in RegCenterArrival.objects.filter(data_day=now.date()):
                    init_dict = dict()
                    if rca.station_number in carrivals_set:
                        init_dict['c' + now.strftime('%H')] = 1
                        carrivals_set.remove(rca.station_number)
                    else:
                        init_dict['c' + now.strftime('%H')] = 0
                    rca.init_from_dict(init_dict)
                    rca.save(force_update=True, update_fields='c' + now.strftime('%H'))
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
                    if ab.station_number in batterys_set:
                        if batterys[ab.station_number] is None:
                            init_dict['b' + now.strftime('%H')] = -1.0
                        else:
                            init_dict['b' + now.strftime('%H')] = float(batterys[ab.station_number])
                        batterys_set.remove(ab.station_number)
                    else:
                        init_dict['b' + now.strftime('%H')] = -1.0
                    ab.init_from_dict(init_dict)
                    ab.save(force_update=True, update_fields='b' + now.strftime('%H'))
                create_objs = []
                for btr in batterys_set:
                    init_dict = dict()
                    init_dict['data_day'] = now.date()
                    init_dict['station_number'] = btr
                    if batterys[btr] is None:
                        init_dict['b' + now.strftime('%H')] = -1.0
                    else:
                        init_dict['b' + now.strftime('%H')] = float(batterys[btr])
                    abattery = AwsBattery()
                    abattery.init_from_dict(init_dict)
                    create_objs.append(abattery)
                AwsBattery.objects.bulk_create(create_objs)

        with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
            with conn.Consumer(record_queue, accept=['json'], callbacks=[_record_regaws]) as consumer:
                while True:
                    try:
                        conn.drain_events()
                    except Exception as e:
                        raise
