from distutils.command.config import config

import RPi.GPIO as GPIO
import ads1115 as ads1115
import gain as gain
from gpiozero import MCP3008

Moisture_Raw   = ads1115.readRaw(config.moistureADPin, gain, sps) # Scale to 10 bits
if (Moisture_Raw > 0x7FFF):
    Moisture_Raw = 0 # Zero out negative Values
Moisture_Raw = Moisture_Raw / 64 # scale to 10 bits

def scaleMoistureCapacitance1(Moisture_Raw, PlantNumber):
    # do the varying scale of the moisture for Capacitance readers
    # do the varying scale of the moisture
    # based on 10 bit values
    # > #0 100%
    #  = #1 0%
    # scale to 0% from there
    #
    if (Moisture_Raw < config.Capacitor1SensorCalibration[PlantNumber][1]):
        Moisture_Humidity = 100
    else:
        Moisture_Humidity = ((config.Capacitor1SensorCalibration[PlantNumber][0] - Moisture_Raw) * 100.0) / (
        config.Capacitor1SensorCalibration[PlantNumber][0] - config.Capacitor1SensorCalibration[PlantNumber][1])

    if (Moisture_Humidity < 0):
        Moisture_Humidity = 0.0
