import simplejson
import urllib
import math


def f_to_c(F):
    C = (F-32)*5/9
    return math.ceil(C*10)/10
def mph_to_kmh(mph):
    kmh = mph * 1.6
    return math.ceil(kmh*10)/10

def avg_data(sources, sensor):
    data_count = 0
    data_sum = 0.0
    for source in sources:
        if getattr(source, sensor) != None:
            data_sum += float(getattr(source, sensor))
            data_count += 1
    result = data_sum / data_count
    rounded_result = math.ceil(result*10)/10
    return rounded_result


class Weather():
    def __init__(self):
        self.pressure = None
        self.windspeed = None
        self.temp = None
        self.precipmm = None
        self.humidity = None

    def parse_wwo_source(self):
        try:
            www = urllib.urlopen("http://api.worldweatheronline.com/free/"
                                 "v1/weather.ashx?key=jh655c6q76smz8m"
                                 "&q=Warszawa,poland&fx=no&format=json").read()
            j = simplejson.loads(www)
        except Exception, e:
            print "[!] Error parsing WorldWeatherOnline.com"
            print "E: " + str(e)
        if j:
            self.pressure = j['data']['current_condition'][0]['pressure']
            self.windspeed = j['data']['current_condition'][0]['windspeedKmph']
            self.temp = j['data']['current_condition'][0]['temp_C']
            self.precipmm = j['data']['current_condition'][0]['precipMM']
            self.humidity = j['data']['current_condition'][0]['humidity']

    def parse_wg(self):
        try:
            www = urllib.urlopen("http://api.wunderground.com/api/"
                                 "f649f9acfee0/conditions/"
                                 "q/Poland/Warszawa.json").read()
            j = simplejson.loads(www)
        except Exception, e:
            print "[!] Error parsing WunderGround.com"
            print "E: " + str(e)
        if j:
            self.pressure = j['current_observation']['pressure_mb']
            self.windspeed = j['current_observation']['wind_kph']
            self.temp = j['current_observation']['temp_c']
            self.precipmm = j['current_observation']['precip_1hr_metric']
            self.humidity = j['current_observation']['relative_humidity']
            self.humidity = self.humidity.replace("%", "")

    def parse_forecast(self):
        try:
            www = urllib.urlopen("https://api.forecast.io/forecast/"
                       "3987773686c00b/"
                       "51.17,19.57").read()
            j = simplejson.loads(www)
        except Exception, e:
            print "[!] Error while parsing WunderGround.com"
            print "E: " + str(e)
        if j:
            self.pressure = j['currently']['pressure']
            self.windspeed = mph_to_kmh(j['currently']['windSpeed'])
            self.temp = f_to_c(j['currently']['temperature'])
            self.precipmm = j['currently']['precipIntensity']
            self.humidity = (j['currently']['humidity'])*100

    def parse_openmap(self):
        try:
            www = urllib.urlopen("http://api.openweathermap.org/data/2.5/"
                                 "weather?q=Warszawa,Poland"
                                 "&units=metric").read()
            j = simplejson.loads(www)
        except Exception, e:
            print "[!] Error while parsing OpenWeatherMap.com"
            print "E: " + str(e)
        if j:
            self.pressure = j['main']['pressure']
            self.windspeed = j['wind']['speed']
            self.temp = j['main']['temp']
            self.humidity = j['main']['humidity']

    def print_values(self):
        print "Pressure: " + str(self.pressure)
        print "Windspeed: " + str(self.windspeed)
        print "Temperature: " + str(self.temp)
        print "MM: " + str(self.precipmm)
        print "Humidity: " + str(self.humidity)