import time
import requests
from pprint import pprint

settings = {
    'api_key':'957ea5e3412c8e4daa0d8f0547b7c716',
    'zip_code':'Dallas',
    'country_code':'us',
    'temp_unit':'metric'} #unit can be metric, imperial, or kelvin

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}"

while True:
    final_url = BASE_URL.format(settings["zip_code"],settings["api_key"],settings["temp_unit"])
    pprint(final_url)
    weather_data = requests.get(final_url).json()
    pprint(weather_data)
    temperature = weather_data['main']['temp']
    pprint(temperature)
    time.sleep(20) #get new data every 20 seconds




