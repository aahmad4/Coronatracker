import json
import threading
import requests
import datetime
import os
import sys
from dateutil import parser
from urllib.request import Request, urlopen
import time
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 9})

countryNames=['USA','Spain','Italy','France','UK','Germany','Turkey','Russia','Iran','Brazil','Canada','Belgium','Netherlands','India','Peru','Switzerland','Portugal','Ecuador','Saudi Arabia','Sweden','Ireland','Mexico','Israel','Singapore','Austria','Pakistan','Chile','Japan','Belarus','Qatar','Poland','Romania','UAE','S. Korea','Ukraine','Indonesia','Denmark','Serbia','Philippines','Norway','Czechia','Bangladesh','Australia','Dominican Republic','Panama','Colombia','Malaysia','Egypt','South Africa','Finland','Morocco','Argentina','Luxembourg','Kuwait','Algeria','Moldova','Kazakhstan','Thailand','Bahrain','Hungary','Greece','Oman','Croatia','Uzbekistan','Afghanistan','Armenia','Iraq','Cameroon','Iceland','Azerbaijan','Bosnia and Herzegovina','Ghana','Estonia','Nigeria','New Zealand','North Macedonia','Bulgaria','Cuba','Slovenia','Slovakia','Lithuania','Guinea','Ivory Coast','Djibouti','Bolivia','Hong Kong','Tunisia','Latvia','Cyprus','Senegal','Albania','Andorra','Honduras','Kyrgyzstan','Lebanon','Diamond Princess','Niger','Costa Rica','Burkina Faso','Uruguay','Sri Lanka','San Marino','Guatemala','Channel Islands','Somalia','Georgia','DRC','Tanzania','Malta','Mayotte','Jordan','Taiwan','Mali','Réunion','Kenya','Jamaica','El Salvador','Palestine','Mauritius','Venezuela','Montenegro','Sudan','Equatorial Guinea','Isle of Man','Vietnam','Maldives','Paraguay','Gabon','Rwanda','Congo','Faeroe Islands','Martinique','Myanmar','Guadeloupe','Liberia','Gibraltar','Brunei','Ethiopia','Madagascar','French Guiana','Cambodia','Trinidad and Tobago','Cabo Verde','Bermuda','Sierra Leone','Aruba','Togo','Zambia','Monaco','Liechtenstein','Bahamas','Barbados','Uganda','Haiti','Mozambique','Sint Maarten','Guyana','Guinea-Bissau','Eswatini','Cayman Islands','Benin','Libya','French Polynesia','Nepal','Chad','CAR','Macao','Syria','Eritrea','Saint Martin','Mongolia','Malawi','South Sudan','Zimbabwe','Angola','Antigua and Barbuda','Timor-Leste','Botswana','Grenada','Laos','Belize','Fiji','New Caledonia','Curaçao','Dominica','Namibia','Saint Kitts and Nevis','Saint Lucia','St. Vincent Grenadines','Nicaragua','Falkland Islands','Turks and Caicos','Burundi','Montserrat','Greenland','Seychelles','Gambia','Suriname','Vatican City','MS Zaandam','Mauritania','Papua New Guinea','Sao Tome and Principe','Bhutan','British Virgin Islands','St. Barth','Western Sahara','Caribbean Netherlands','Anguilla','Saint Pierre Miquelon','Yemen','China']
lowerCountryNames=[x.lower() for x in countryNames]

def fixCountryNames(name):
    return countryNames[lowerCountryNames.index(name)]

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
    plt.plot(xvals[-10:],yvals[-10:],label=fixCountryNames(country))
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
    plt.title("Statistics in " + fixCountryNames(country))
    plt.legend()
    plt.savefig("/tmp/c/"+country+"__bar.png")


def comp(country1,country2,json_data1,json_data2):
    
    data1=lineValsGen(fixCountryNames(country1),json_data1)
    xvals1=data1[0]
    yvals1=data1[1]
    
    data2=lineValsGen(fixCountryNames(country2),json_data2)
    xvals2=data2[0]
    yvals2=data2[1]
    
    title = "Number of Active Cases of COVID-19"
    plt.title(title)
    plt.ylabel("Active Cases")
    plt.xlabel("Date")
    plt.plot(xvals1[-10:],yvals1[-10:],label=fixCountryNames(country1))
    plt.plot(xvals2[-10:],yvals2[-10:],label=fixCountryNames(country2))
    plt.legend()
    plt.savefig("/tmp/c/"+country1+"_"+country2+"__comp.png")

def apiReq(countries):
    apiArr=[]
    for item in countries:
        querystring = {"country":fixCountryNames(item)}
    
        headers = {
            'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
            'x-rapidapi-key': os.environ["apikey"] # security measure, see ".env" in files to find the key
            }

        response = requests.request("GET", "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php", headers=headers, params=querystring)

        json_data = response.json()
        
        json_data = json_data.values()

        #json_data = json_data['stat_by_country']

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
