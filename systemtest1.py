from datetime import datetime
import time
import requests
from pprint import pprint
#import RPi.GPIO as GPIO
import time

itstime = datetime.now()
settings = {
    #Revoked API Key
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
    #t0 = time.clock_gettime_ns( time.CLOCK_REALTIME)
    temperature = weather_data['main']['temp']
    pprint(weather_data['weather'][0]['description'])
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