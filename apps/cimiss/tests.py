from django.test import TestCase

# Create your tests here.

import random, datetime
import time
from django.db.models import Q
from .models import AwsArrival

# from apscheduler.schedulers.background import BackgroundScheduler
#
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
#
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(scheduler, "interval", seconds=5, replace_existing=True, id='666')
def test_job():
    print("I'm a test job!")
    a = dict()
    a['data_day'] = datetime.datetime.utcnow().date()
    a['station_number'] = 'J0003'
    a['a01'] = 1
    awsarrival = AwsArrival()
    awsarrival.init_from_dict(a)
    try:
        awsarrival.save()
    except Exception as e:
        print(e)
    q = Q()
    q.connector = 'AND'
    q.children.append(('data_day', datetime.datetime.utcnow().date()))
    q.children.append(('a01', 1))
    try:
        arrivals = AwsArrival.objects.filter(q)
    except Exception as e:
        pass

    print(len(arrivals))
    time.sleep(1)


# register_events(scheduler)

# scheduler.start()
# print("Scheduler started!")
