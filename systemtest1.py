from datetime import datetime
import time
import requests
from pprint import pprint
#import RPi.GPIO as GPIO
import time

itstime = datetime.now()
settings = {
    'api_key':'957ea5e3412c8e4daa0d8f0547b7c716',
    'zip_code':'Dallas',
    'country_code':'us',
    'temp_unit':'metric'}
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}"
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(18,GPIO.OUT)
#GPIO.setup(17,GPIO.OUT)
#GPIO.setup(16,GPIO.OUT)

while True:
    final_url = BASE_URL.format(settings["zip_code"], settings["api_key"], settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    pprint(weather_data)
    temperature = weather_data['main']['temp']
    if temperature >= 0:
        second = itstime.second
        pprint(second)
        if second % 2 == 0:
            pprint("1 on")
            #GPIO.output(18, GPIO.HIGH)
            #GPIO.output(17, GPIO.LOW)
            #GPIO.output(16, GPIO.LOW)
        if second % 3 == 0:
            pprint("2 on")
            #GPIO.output(18, GPIO.LOW)
            #GPIO.output(17, GPIO.HIGH)
            #GPIO.output(16, GPIO.LOW)
        if second % 5 == 0:
            pprint("3 on")
            #GPIO.output(18, GPIO.LOW)
            #GPIO.output(17, GPIO.LOW)
            #GPIO.output(16, GPIO.HIGH)
    time.sleep(5)  # get new data every 20 seconds