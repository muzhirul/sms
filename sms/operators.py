# from time import sleep
# # from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
# from apscheduler.schedulers.background import BlockingScheduler,BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoJobStore
# from sms.scheduledapi import attendence_loader

# def data_insert_start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
#     register_events(scheduler)

#     @scheduler.scheduled_job('interval', seconds=60, name='insert_data')
#     def insert_data():
#         attendence_loader()
#     scheduler.start()

# def display():
#     print('This function has been executed')

# scheduler = BlockingScheduler()
# scheduler.add_job(display, 'interval', seconds = 1)
# scheduler.start()

from time import sleep
import requests
from django.contrib.sites.shortcuts import get_current_site
from apscheduler.schedulers.background import BlockingScheduler
from decouple import config

def display():
    # current_site = get_current_site(request).domain
    urlList = ["/student/api/attendance/process","/staff/api/attendance/process"]
    for urlpath in urlList:
        # print(urlpath)
        url = f"{config('BASE_URL')}"+urlpath
        print(url)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
    # url = f"http://192.168.9.20:8000/student/api/attendance/process"
    # payload = {}
    # headers = {}
    # response = requests.request("GET", url, headers=headers, data=payload)
    # print('current_site')

scheduler = BlockingScheduler()
scheduler.add_job(display,'interval', seconds = 60)
scheduler.start()