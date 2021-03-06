import json
import requests
from datetime import date, datetime
from collections import OrderedDict
from threading import Timer
form email_alert import *

def extract_data():
    output=""
    today = date.today()
    date_today = today.strftime("%d-%m-%Y")
    date_today = date_today.strip()
    time_curr = datetime.now().strftime("%H:%M:%S")
    pincode = "248001" #example pincode
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date_today}"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}  #can add more headers but user-agent is compulsory 

    response = requests.get(url, headers= headers)


    siteJson = json.loads(response.text)
    centers = siteJson['centers']

    for i in centers:
        center_id = i["center_id"]
        sessions = i["sessions"]
        output_each_session = {}
        for j in sessions:
            output+="\n"
            output_each_session["center_id"] = center_id
            output_each_session["center_name"] = i["name"]
            output_each_session["center_address"] = i["address"] +" "+ i["district_name"] + " " + i["state_name"]
            output_each_session["pincode"] = i["pincode"]
            output_each_session["fee_type"] = i["fee_type"]
            output_each_session["date"] = j["date"]
            output_each_session["available_capacity"] = j["available_capacity"]
            output_each_session["min_age_limit"] = j["min_age_limit"]
            output_each_session["vaccine_name"] = j["vaccine"]
            output_each_session["slots"] = j["slots"]

            if output_each_session["min_age_limit"] == 18 and output_each_session["available_capacity"] != 0 and output_each_session["center_id"] == "190290": #desired center id 
                output_each_session = OrderedDict(output_each_session)
                for key, val in output_each_session.items():
                    output += str(key) + " : " + str(val)+ "\n"
    
    output = output.strip()
    if len(output) != 0:
        emailalert(pincode, output)
        return
    else:
        print(f"Will retry in a minute. Last tried: {time_curr}")
    Timer(60, extract_data).start() #will check every minute when script is runnning

extract_data()
