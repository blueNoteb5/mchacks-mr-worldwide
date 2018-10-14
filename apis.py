import urllib.request
import urllib.parse
import json
from iso639 import languages #https://pypi.python.org/pypi/iso-639. Converts from normal text to ISO codes
from forecastiopy import * #Using library https://github.com/bitpixdigital/forecastiopy3 and DarkSky API
import re #for converting to plaintext from HTML
import requests

#API keys, you need to insert your own!
bing_apikey = "" #for Bing search API
translate_apikey = ""
directions_apikey = ""
weather_apikey = ""
geocode_apikey = ""

assert bing_apikey #for Bing search API

#Gets current weather.
def getWeather(city):

    #Parses into html string
    query=city
    toParse = {"address" : query}
    query = urllib.parse.urlencode(toParse)

    #Gets latitude and longitude using google geocode API
    json.html=urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?" + query + "&key=" + geocode_apikey).read()
    htmlData=json.loads(json.html)
    lat = (htmlData['results'][0]['geometry']['location']['lat'])
    lng = (htmlData['results'][0]['geometry']['location']['lng'])

    City = [lat, lng]
    fio = ForecastIO.ForecastIO(weather_apikey, units=ForecastIO.ForecastIO.UNITS_SI, lang=ForecastIO.ForecastIO.LANG_ENGLISH, latitude=City[0], longitude=City[1])

    if fio.has_currently() is True:
        currently = FIOCurrently.FIOCurrently(fio)
        if fio.has_hourly() is True:
            hourly = FIOHourly.FIOHourly(fio)
            weather = ("Currently it is %s degrees Celsius. %s" % (currently.temperature, hourly.summary))
        else:
            weather = ("Currently it is %s degrees Celsius." % currently.temperature)
    else:
        weather = 'No Current data available'
    return(weather)


#Google translate. Language has to start with capital.
def translate(toTranslate, language):

    target=languages.get(name=language.title())
    target = target.alpha2
    query=toTranslate
    toParse = {"q" : query}
    query = urllib.parse.urlencode(toParse)

    json.html=urllib.request.urlopen("https://translation.googleapis.com/language/translate/v2?" + query + "&target=" + target + "&key=" + translate_apikey).read()
    htmlData=json.loads(json.html)
    result = (htmlData['data']['translations'][0]['translatedText'])
    return(result)

#Gets directions in text format using google directions api
#mode options: driving(default), walking, bicycling, transit
def getDirections(origin, destination, mode):
    try:
        toParse = {"origin" : origin, "destination" : destination, "mode" : mode}
        query = urllib.parse.urlencode(toParse)
        json.html=urllib.request.urlopen(
        "https://maps.googleapis.com/maps/api/directions/json?"+query+"&key=" + directions_apikey).read()
        resp=json.loads(json.html)
        data = ""
        cleanResp = ""
        for x in range(0,len(resp['routes'][0]['legs'][0]['steps'])):
                data = (resp['routes'][0]['legs'][0]['steps'][x]['html_instructions'])
                cleanData = re.sub(r'<.*?>', '', data)
                cleanResp = cleanResp + '\n' + cleanData
                if x>300:
                    message = "Destination is too far for SMS directions"
                    return message

        return cleanResp
    except IndexError:
        message = "please enter a valid route"
        return message

def getNews(location):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    search_term = location
    headers = {"Ocp-Apim-Subscription-Key" : bing_apikey}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count" : '1', "offset" : '0'}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    descriptions = [article["description"] for article in search_results["value"]]
    cleanResp = ""
    for x in range(len(descriptions)):
        data = (descriptions[x])
        cleanData = re.sub(r'<.*?>', '', data)
        cleanData = re.sub(r'&quot', '"', cleanData)
        cleanData = re.sub(r'&#39', "'", cleanData)
        cleanResp = cleanResp + '\n\n' + cleanData
        cleanData = re.sub(r';', " ", cleanData)

    return(cleanResp)
