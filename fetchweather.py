import time
import requests
from pprint import pprint

settings = {
    'api_key':'957ea5e3412c8e4daa0d8f0547b7c716',
    'zip_code':'75072',
    'country_code':'us',
    'temp_unit':'imperial'} #unit can be metric, imperial, or kelvin

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"

while True:
    final_url = BASE_URL.format(settings["api_key"],settings["zip_code"],settings["country_code"],settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    pprint(weather_data)
    time.sleep(20) #get new data every 20 seconds
    #temperature = weather_data[“main”][“temp”]



