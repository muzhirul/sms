from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from sms.scheduledapi import attendence_loader

def data_insert_start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', seconds=60, name='insert_data')
    def insert_data():
        attendence_loader()
    scheduler.start()

# def display():
#     print('This function has been executed')

# schedular = BlockingScheduler()
# schedular.add_job(display, 'interval', seconds = 1)
# schedular.start()