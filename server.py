import json
import threading
import requests
import matplotlib.pyplot as plt
import datetime
import os
import sys
from dateutil import parser
from urllib.request import Request, urlopen
import time

def lineValsGen(country,json_data):
    xvals = []
    yvals = []
    
    for item in json_data:
        date = item['record_date'][6:10]
        tdy = datetime.date.today()
        
        if date in xvals:
            pass
        else:
            xvals.append(date)
            yvals.append( int(item["active_cases"].replace(",","")) )
    
    xvals.reverse()
    yvals.reverse()
    return [xvals,yvals]

def graph(country,json_data):
    data=lineValsGen(country,json_data)
    xvals=data[0]
    yvals=data[1]
    
    title = "Number of Active Cases of COVID-19"
    plt.title(title)
    plt.ylabel("Active Cases")
    plt.xlabel("Date")
    plt.plot(xvals,yvals,label=country.title())
    plt.legend()
    plt.savefig("/tmp/c/"+country+".png")
    
    

def bar(country,json_data):
    labels = ["Total Cases","Total Deaths","Total Recoveries"]
    totCases=json_data[0]["total_cases"].replace(",","")
    totDeaths=json_data[0]["total_deaths"].replace(",","")
    totRecov=json_data[0]["total_recovered"].replace(",","")
    values = [int(totCases) if totCases else 0,int(totDeaths) if totDeaths else 0,int(totRecov) if totRecov else 0]
    plt.bar(labels[0],values[0],label=labels[0])
    plt.bar(labels[1],values[1],label=labels[1])
    plt.bar(labels[2],values[2],label=labels[2])
    plt.title("Statistics in " + country.title())
    plt.legend()
    plt.savefig("/tmp/c/"+country+"__bar.png")


def comp(country1,country2,json_data1,json_data2):
    
    data1=lineValsGen(country1,json_data1)
    xvals1=data1[0]
    yvals1=data1[1]
    
    data2=lineValsGen(country2,json_data2)
    xvals2=data2[0]
    yvals2=data2[1]
    
    title = "Number of Active Cases of COVID-19"
    plt.title(title)
    plt.ylabel("Active Cases")
    plt.xlabel("Date")
    plt.plot(xvals1,yvals1,label=country1.title())
    plt.plot(xvals2,yvals2,label=country2.title())
    plt.legend()
    plt.savefig("/tmp/c/"+country1+"_"+country2+"__comp.png")

def apiReq(countries):
    apiArr=[]
    for item in countries:
        querystring = {"country":item}
    
        headers = {
            'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
            'x-rapidapi-key': os.environ["apikey"] # security measure, see ".env" in files to find the key
            }

        response = requests.request("GET", "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php", headers=headers, params=querystring)

        json_data = response.json()

        data_length = len(json_data['stat_by_country'])#not entirely sure this is ever used lol

        json_data = json_data['stat_by_country']

        json_data = sorted(json_data, key=lambda k: k['record_date']) 
        json_data.reverse()
        apiArr.append(json_data)
    return apiArr

arg1=sys.argv[1].lower()
isBar=arg1.endswith("__bar")
isComp=arg1.endswith("__comp")

#this if statement is the time restriction to update every hour
if not os.path.exists("/tmp/c/"+arg1+".png") or os.path.getmtime("/tmp/c/"+arg1+".png")-time.time()>3600:
    if isBar:
        arg1=arg1.replace("__bar","")
    if isComp:
        arg1=arg1.replace("__comp","")
    
    
    if isBar:
        bar(arg1,apiReq([arg1])[0])
    elif isComp:
        spl=arg1.split("_")
        apiRes=apiReq(spl)
        comp(spl[0],spl[1],apiRes[0],apiRes[1])
    else:
        graph(arg1,apiReq([arg1])[0])