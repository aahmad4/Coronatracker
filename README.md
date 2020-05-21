# Live Coronavirus Tracker
A live coronavirus tracking website, made with a back-end of Node.js / Python and a front-end of HTML / CSS, which tracks international data on the COVID-19 pandemic and displays it in easy to read graphics. We hosted the website on glitch and the link can be found [here](https://coronatracker.glitch.me/) or below.

https://coronatracker.glitch.me/

## Repository Contents
* [server.js](https://github.com/aahmad4/Live-Coronavirus-Tracker/blob/master/server.js): This contains our first back-end programming file which was written in Node.js. This file contains the web server and assets to run the python aspect and return the images of data to the end-user.
* [server.py](https://github.com/aahmad4/Live-Coronavirus-Tracker/blob/master/server.py): This is our second back-end programming language. This file contains the logic for the server to communicate with the JavaScript and HTML. Also, this is where we have the logic written for using the Coronavirus Monitor Rapid API to make our own graphs with matplotlib and distrubute them to the end-user.
* [index.html](https://github.com/aahmad4/Live-Coronavirus-Tracker/blob/master/public/index.html) and [style.css](https://github.com/aahmad4/Live-Coronavirus-Tracker/blob/master/public/style.css) in the public folder both contain the front-end of the website and that's where the user interface and overall design of the website was developed.

## How To Use
To use our Coronavirus tracker, simply use our drop drown and select any country you'd like, and instantly view live statistics regarding the disease in that country. We have another feature that allows the end-user to compare the amount of people with the disease in multiple countries.

(Note: All statistics of Coronavirus are updated roughly once an hour)


## Screenshots of Website

![](screenshot1.png)

![](screenshot2.png)


## Clone
```bash
git clone https://github.com/aahmad4/Live-Coronavirus-Tracker
```

## Implementation

In [server.py](https://github.com/aahmad4/Live-Coronavirus-Tracker/blob/master/server.py), change `"apikey"` to match your personal key on Rapid API.
```python
def apiReq(countries):
    apiArr=[]
    for item in countries:
        querystring = {"country":fixCountryNames(item)}
        
        headers = {
            'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
            'x-rapidapi-key': os.environ["apikey"] # security measure, see ".env" in files to find the key
            }
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
