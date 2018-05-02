from apscheduler.schedulers.background import BackgroundScheduler
from apps.cimiss.tests import test_job


scheduler = BackgroundScheduler()

scheduler.add_job(test_job, "interval", seconds=5, id='555')

scheduler.start()
