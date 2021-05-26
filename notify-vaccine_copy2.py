import requests
import json
#from notify_run import Notify
#from datetime import date
from datetime import datetime, timedelta
import time
from requests.structures import CaseInsensitiveDict

url_send = "https://notify.run/Obq6PY3uUJqdefes"
url_check = "https://notify.run/I5WmkbTrrfqJ6vU7"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
data1 = "cron job start_check" + str(current_time)


resp = requests.post(url_check, headers=headers, data=data1)

#print(resp.status_code)
#notify = Notify()

#notify.send("check")
n=0

for k in range(118):
    now = datetime.now()
    d1 = now.strftime("%d-%m-%Y")
    pin = "294"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    url ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(pin)+"&date="+str(d1)
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Website Error")
        continue
    data = response.text

    parsed = json.loads(data)

    
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    
    if(n%30==0):
        message = "Runtime Check on " + str(current_time)
        resp = requests.post(url_check, headers=headers, data=message)
        print("sent runtime check")
    n=n+1
    n_centers = len(parsed["centers"])
    for i in range(n_centers):
        n_sessions = len(parsed["centers"][i]["sessions"])
        for j in range(n_sessions):
            if(parsed["centers"][i]["sessions"][j]["min_age_limit"] == 18):
                print("Min age 18 At "+str(parsed["centers"][i]["name"])+ " on " + str(parsed["centers"][i]["sessions"][j]["date"]) + " available capacity is " + str(parsed["centers"][i]["sessions"][j]["available_capacity"]) )
                capacity = parsed["centers"][i]["sessions"][j]["available_capacity"]
                message = "Pincode:"+str(parsed["centers"][i]["pincode"])+" Available capacity is " + str(parsed["centers"][i]["sessions"][j]["available_capacity"]) + " at "+str(parsed["centers"][i]["name"])+ " on " + str(parsed["centers"][i]["sessions"][j]["date"])
                if (capacity > 0):
                    resp = requests.post(url_send, headers=headers, data=message)
                    otpheaders = {
                        'accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                    
                    bikramdata = '{"mobile":"7338016027"}'
                    janhavidata = '{"mobile":"8105994097"}'
                    kesavdata = '{"mobile":"990212932"}'
                    
                    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=otpheaders, data=bikramdata)
                    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=otpheaders, data=janhavidata)
                    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=otpheaders, data=kesavdata)


    time.sleep(1)
