import requests
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from decouple import config

# current_site = get_current_site(request).domain
# SITE_PROTOCOL = 'http://'
#     if request.is_secure():
#         SITE_PROTOCOL = 'https://'

def attendence_loader():
    # url = f"http://127.0.0.1:8000/student/api/attendance/process"
    urlList = ["/student/api/attendance/process","/staff/api/attendance/process"]
    url = f"{config('BASE_URL')}/student/api/attendance/process"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print('Insert student attendanc process DONE')