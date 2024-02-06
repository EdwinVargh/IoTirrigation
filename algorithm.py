import time
from pprint import pprint

import requests

infil = {"sand": 1.5, "loamy sand": 1, "sandy loam": 0.8, "loam": 0.4, "silty loam": 0.25, "silt": 0.3,
         "sandy clay loam": 0.1, "clay loam": 0.07, "silty clay loam": 0.05, "sandy clay": 0.08, "silty clay": 0.05,
         "clay": 0.05}
plantavail = {"sand": 0.05, "loamy sand": 0.07, "sandy loam": 0.11, "loam": 0.16, "silty loam": 0.2, "silt": 0.2,
              "sandy clay loam": 0.15, "clay loam": 0.16, "silty clay loam": 0.18, "sandy clay": 0.12,
              "silty clay": 0.14, "clay": 0.15}
runcos = {"sand": 0.17, "loamy sand": 0.21, "sandy loam": 0.24, "loam": 0.27, "silty loam": 0.31, "silt": 0.34,
              "sandy clay loam": 0.37, "clay loam": 0.41, "silty clay loam": 0.44, "sandy clay": 0.47,
              "silty clay": 0.51, "clay": 0.54}

area = 100 #entered

settings = {
    'api_key':'957ea5e3412c8e4daa0d8f0547b7c716',
    'zip_code':'Dallas',
    'country_code':'us',
    'temp_unit':'metric'} #unit can be metric, imperial, or kelvin

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}"
final_url = BASE_URL.format(settings["zip_code"], settings["api_key"], settings["temp_unit"])
weather_data = requests.get(final_url).json()
while True:
    soil = "clay loam"
    zones = 5 #entered
    flowrate = 4 #based on sprinkler head entered
    depthwet = 6
    preciprate = flowrate*zones*1.604/area
    schedmult = 0.39 #predict with machine learning
    maxhumidratio = 0.007 #predict with machine learning
    runco = runcos[soil]

    runtime2 = ((0.623*area)+(25+19*weather_data['wind']['speed'])*area*(maxhumidratio-maxhumidratio*.01*weather_data['main']['humidity'])*0.000264172052)/flowrate
    runtime = (depthwet*plantavail[soil])/(preciprate*schedmult*2)
    pprint(runtime2)
    pprint(runtime)
    time.sleep(5)
