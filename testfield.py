import simplejson
import urllib
from weather import Weather, avg_data


first = Weather()
first.parse_wg()
second = Weather()
second.parse_wwo_source()
third = Weather()
third.parse_forecast()
forth = Weather()
forth.parse_openmap()
sensors = ['pressure', 'windspeed', 'temp', 'precipmm', 'humidity']
sources = []
sources.append(first)
sources.append(second)
sources.append(third)
sources.append(forth)

for sensor in sensors:
    print sensor + ": "
    weather.avg_data(sources, sensor)