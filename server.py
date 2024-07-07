import json
import threading
import requests
import datetime
import os
import sys
from dateutil import parser
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 9})

with open('countriesSlug.json', 'r') as slcfile:
    slcjson = json.loads(slcfile.read())

slcjson = {slcjson[k]: k for k in slcjson}


def lineValsGen(country, json_data):
    xvals = []
    yvals = []

    for item in json_data:
        if not isinstance(item, dict):
            continue

        date = item['date'][5:10]

        if date in xvals:
            pass
        else:
            xvals.append(date)
            yvals.append(item["active"])

    xvals.reverse()
    yvals.reverse()
    return [xvals, yvals]


def graph(country, json_data):
    data = lineValsGen(country, json_data)
    xvals = data[0]
    yvals = data[1]

    title = "Number of Active Cases of COVID-19"
    plt.title(title)
    plt.ylabel("Active Cases")
    plt.xlabel("Date")
    plt.plot(xvals[-10:], yvals[-10:], label=slcjson[country.upper()])
    plt.legend()
    plt.savefig("/tmp/c/"+country+".png")


def bar(country, json_data):
    labels = ["Total Cases", "Total Deaths", "Total Recoveries"]
    totCases = json_data[0]["confirmed"]
    totDeaths = json_data[0]["deaths"]
    totRecov = json_data[0]["recovered"]
    values = [int(totCases) if totCases else 0, int(totDeaths)
              if totDeaths else 0, int(totRecov) if totRecov else 0]
    plt.bar(labels[0], values[0], label=labels[0])
    plt.bar(labels[1], values[1], label=labels[1])
    plt.bar(labels[2], values[2], label=labels[2])
    plt.title("Statistics in " + slcjson[country.upper()])
    plt.legend()
    plt.savefig("/tmp/c/"+country+"__bar.png")


def comp(country1, country2, json_data1, json_data2):

    data1 = lineValsGen(slcjson[country1.upper()], json_data1)
    xvals1 = data1[0]
    yvals1 = data1[1]

    data2 = lineValsGen(slcjson[country2.upper()], json_data2)
    xvals2 = data2[0]
    yvals2 = data2[1]

    title = "Number of Active Cases of COVID-19"
    plt.title(title)
    plt.ylabel("Active Cases")
    plt.xlabel("Date")
    plt.plot(xvals1[-10:], yvals1[-10:], label=slcjson[country1.upper()])
    plt.plot(xvals2[-10:], yvals2[-10:], label=slcjson[country2.upper()])
    plt.legend()
    plt.savefig("/tmp/c/"+country1+"_"+country2+"__comp.png")


def apiReq(countries):
    today = datetime(2022, datetime.today().month, datetime.today().day)
    # Get the last 7 dates including today
    last_7_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    apiArr = []
    for item in countries:
        all_json_data = []
        for date in last_7_dates:
            response = requests.request(
            "GET", "https://covid-api.com/api/reports/total?date=" + date + "&iso=" + item)
            json_data = response.json()
            all_json_data.append(json_data["data"])
        if (all_json_data):
            all_json_data = sorted(all_json_data, key=lambda k: k['date'])
            all_json_data.reverse()
        apiArr.append(all_json_data)
    return apiArr


arg1 = sys.argv[1].lower()
isBar = arg1.endswith("__bar")
isComp = arg1.endswith("__comp")

# this if statement is the time restriction to update every hour
if not os.path.exists("/tmp/c/"+arg1+".png") or os.path.getmtime("/tmp/c/"+arg1+".png")-time.time() > 3600:
    if isBar:
        arg1 = arg1.replace("__bar", "")
    if isComp:
        arg1 = arg1.replace("__comp", "")

    if isBar:
        bar(arg1, apiReq([arg1])[0])
    elif isComp:
        spl = arg1.split("_")
        apiRes = apiReq(spl)
        comp(spl[0], spl[1], apiRes[0], apiRes[1])
    else:
        graph(arg1, apiReq([arg1])[0])
