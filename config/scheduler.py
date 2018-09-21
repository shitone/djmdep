from apscheduler.schedulers.background import BackgroundScheduler
from apps.cimiss.tasks import reg_notice_task


scheduler = BackgroundScheduler()

scheduler.add_job(reg_notice_task, "cron", minute='15', id='reg_notice')

scheduler.start()