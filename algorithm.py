import time
from pprint import pprint
from matplotlib import pyplot
import numpy
import serial
import time
import datetime
import struct
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as gpio
#import RPi.GPIO as GPIO
#from scipy.interpolate import spline
import guicode
import requests

infil2 = [1.5,0.4,0.3,0.05]
plantavail2 = [0.05,0.16,0.2,0.15]
settings = {
    'api_key':'957ea5e3412c8e4daa0d8f0547b7c716',
    'zip_code':'Dallas',
    'country_code':'us',
    'temp_unit':'metric'} #unit can be metric, imperial, or kelvin
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}"

def InitRtcWithIrq(IrqAlrmPin):
    # Set to Broadcom Pin Number system
    gpio.setmode(gpio.BCM)

    # Configure the RTC for 24Hr time
    bus.write_byte_data(RtcI2cAddr, 0x00, 0x00)
    # Clear Alarm bit in Control Register 2
    bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
    # Leave Control Register 3 set to defaults
    bus.write_byte_data(RtcI2cAddr, 0x02, 0x00)
    # Disable CLKOUT so it doesn't drive /INT1 pin
    bus.write_byte_data(RtcI2cAddr, 0x0F, 0x38)
    # Configure gpio pin to interrupt on alarm
    gpio.setup(IrqAlrmPin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(IrqAlrmPin, gpio.FALLING, callback=rtc_alarm_callback)

AdcI2cAddr = 0x48

AdcConvReg = 0x00
AdcCfgReg = 0x01
AdcCompLoReg = 0x02
AdcCompHiReg = 0x03
bus = SMBus(1)

AdcConfig=[0x42,0x00]
bus.write_i2c_block_data(AdcI2cAddr,AdcCfgReg,AdcConfig)
bus.write_byte(AdcI2cAddr,AdcConvReg)
def rtc_alarm_callback(channel):
    # Clear Alarm in Control Register 2
    bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
    # Set the Alarm on RTC to Monday at 17:01 24hr time (5:01 PM)
    print("RTC Alarm Triggered")
    Mytime = rtc_GetTime()
def BCDtoDec_byte(Bcdval):
    #   developed for working with bytes only
    if (Bcdval == 0):
        return 0x00
    hnib = (Bcdval // 16) * 16
    dec = (Bcdval // 16) * 10
    dec = dec + (Bcdval - hnib)
    return dec

def DectoBCD_byte(decval):
    #   developed for working with bytes only
    if (decval == 0):
        return 0x00
    bcd = 0x00;
    bcd = decval // 10 * 16
    bcd = bcd + (decval % 10)
    return bcd

def rtc_GetTime():
    MyTime = bus.read_i2c_block_data(RtcI2cAddr, 0x03)
    RtnTime = [BCDtoDec_byte(MyTime[4]), BCDtoDec_byte(MyTime[5]), BCDtoDec_byte(MyTime[3]), BCDtoDec_byte(MyTime[6]),
               BCDtoDec_byte(MyTime[2]), BCDtoDec_byte(MyTime[1]), BCDtoDec_byte(MyTime[0])]
    return RtnTime

Msg = i2c_msg.read(AdcI2cAddr, 2)

RtcI2cAddr = 0x68
# RTC is on I2C channel 1
bus = SMBus(1)
# RTCs Alarm pin is connected to GPIO 23
RtcAlrmPin = 23
# Set to Broadcom Pin Number system
gpio.setmode(gpio.BCM)

# Configure the RTC for 12Hr time, enable Alarm in Control Register 1
bus.write_byte_data(RtcI2cAddr, 0x00, 0x08)
# Clear Alarm bit in Control Register 2
bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
# Leave Control Register 3 set to defaults
bus.write_byte_data(RtcI2cAddr, 0x02, 0x00)

def InitMoistureAdc():
    # RTC is on I2C channel 1
    bus = SMBus(1)
    # Configure the ADC for Single Ended, +/-4.096V range, Continuous-conversion, 8SPS, Comp - default
    AdcConfig = [0x42, 0x00]
    bus.write_i2c_block_data(AdcI2cAddr, AdcCfgReg, AdcConfig)
    # Set address pointer to ADC data register
    bus.write_byte(AdcI2cAddr, AdcConvReg)

def ReadMoistureAdc():
    bus = SMBus(1)
    Msg = i2c_msg.read(AdcI2cAddr, 2)
    bus.i2c_rdwr(Msg)
    b = list(Msg)
    val = b[0] * 256 + b[1]

    return (val * 0.000127)

# Configure gpio pin to interrupt on alarm
gpio.setup(RtcAlrmPin, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.add_event_detect(RtcAlrmPin, gpio.FALLING, callback=rtc_alarm_callback)
gpios = [16,19,20,21,26]

date = datetime.now().strftime("%H:%M:%S")
today = datetime.today().strftime("%B:%D:%Y")
wkday = int(datetime.today().weekday())
hr = int(datetime.now().strftime("%H"))
mins = int(datetime.now().strftime("%M"))
sec = int(datetime.now().strftime("%S"))
mon = int(datetime.today().strftime("%B"))
day = int(datetime.today().strftime("%D"))
year = int(datetime.today().strftime("%Y"))-2000

def isDiqual(data):
    weather_data = data
    diqualcount = 0
    if weather_data['main']['temp'] >= 35:
        diqualcount += 1
    if weather_data['main']['temp'] <= 0:
        diqualcount += 1
    if weather_data['main']['humidity'] > 80:
        diqualcount += 1
    lightrain = weather_data['weather'][0]['description'] == 'light rain'
    modrain = weather_data['weather'][0]['description'] == 'moderate rain'
    heavyrain = weather_data['weather'][0]['description'] == 'heavy intensity rain'
    rainsnow = weather_data['weather'][0]['description'] == 'rain and snow'
    if lightrain or modrain or heavyrain or rainsnow:
        diqualcount += 1
    if ReadMoistureAdc() > 1.5:
        diqualcount += 1
    return diqualcount

def rtc_set_alarm_datetime(Wkday, months, Mthday, years, hours, minutes, seconds):
    MyTime = [DectoBCD_byte(seconds), DectoBCD_byte(minutes), DectoBCD_byte(hours), DectoBCD_byte(Mthday),
              DectoBCD_byte(Wkday), DectoBCD_byte(months), DectoBCD_byte(years)]
    bus.write_i2c_block_data(RtcI2cAddr, 0x0A, MyTime)
def rtc_set_datetime(Wkday, months, Mthday, years, hours, minutes, seconds):
    MyTime = [DectoBCD_byte(seconds), DectoBCD_byte(minutes), DectoBCD_byte(hours), DectoBCD_byte(Mthday),
              DectoBCD_byte(Wkday), DectoBCD_byte(months), DectoBCD_byte(years)]
    bus.write_i2c_block_data(RtcI2cAddr, 0x03, MyTime)

rtc_set_datetime(wkday,mon,day,year,hr,mins,sec)
HdrLen = 4
port = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE, timeout=1.0)
InitMoistureAdc()
def main():
    global ValEndHr
    while True:
        MoistureVolts = ReadMoistureAdc()
        fdata = struct.pack("f", MoistureVolts)
        port.write(fdata)
        time.sleep(0.2)

        num_bytes = port.inWaiting()
        grasses = 0
        soils = 0
        days = [] #stores what days are available
        if num_bytes >= HdrLen: #unpacks received GUI information
            print("Number of Bytes received = ", num_bytes)
            # cPktId = port.read(HdrLen)
            iPktId = struct.unpack('i', port.read(HdrLen))
            # check if packet is a configuration change command
            if ((iPktId[0] & 0xFF000000) == 0x57000000):
                PktLen = ((iPktId[0] & 0x000000FF) - HdrLen)
                time.sleep(0.5)
                num_bytes = port.inWaiting()
                if (num_bytes < PktLen):
                    print("Expected ", PktLen, "bytes on serial port, only received ", num_bytes)
                    break
                else:
                    rx_data = port.read(PktLen)
                    fdata = struct.unpack_from('f', rx_data, offset=0)
                    FlowRate = fdata[0]
                    ValidDays = ord((struct.unpack_from('c', rx_data, offset=4))[0])
                    if (ValidDays >> 5) & 0x01:
                        days.append(0)
                    if (ValidDays >> 4) & 0x01:
                        days.append(1)
                    if (ValidDays >> 3) & 0x01:
                        days.append(2)
                    if (ValidDays >> 2) & 0x01:
                        days.append(3)
                    if (ValidDays >> 1) & 0x01:
                        days.append(4)
                    if ValidDays & 0x01:
                        days.append(5)
                    if (ValidDays >> 6) & 0x01:
                        days.append(6)
                    ValBegHr = ord((struct.unpack_from('c', rx_data, offset=5))[0])
                    ValBegMin = ord((struct.unpack_from('c', rx_data, offset=6))[0])
                    ValEndHr = ord((struct.unpack_from('c', rx_data, offset=8))[0])
                    ValEndMin = ord((struct.unpack_from('c', rx_data, offset=9))[0])
                    Zone = ord((struct.unpack_from('c', rx_data, offset=11))[0])
                    grasses = (Zone >> 4) & 0x0F
                    soils = Zone & 0x0F
            if ((iPktId[0] & 0xFF000000) == 0x77000000):
                runprof = iPktId[0] & 0x000000FF

        gpio.setup(RtcAlrmPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(RtcAlrmPin, gpio.FALLING, callback=rtc_alarm_callback)

        # Set the time and date on RTC to Monday, May 11, 1964 @ 4:59:00PM
        i=0
        dayof = 0
        for x in days:
            if x >= dayof:
                dayof = i
            i+=1
        rtc_set_alarm_datetime(days[dayof], mon, day+(days[dayof]-wkday), year, ValBegHr, ValBegMin, 0)
        time.sleep(0.5)
        alarm = bus.read_byte_data(RtcI2cAddr, 0x01)
        alarm2 = gpio.input(RtcAlrmPin)
        if alarm2 == gpio.LOW:
            bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
        print("Alarm Reg: ", alarm, "Pin: ", alarm2)
        final_url = BASE_URL.format(settings["zip_code"], settings["api_key"], settings["temp_unit"]) #Gets weather data
        weather_data = requests.get(final_url).json()
        area = 50  # based on sprinkler head
        x = numpy.array([0, 5, 10, 15, 20, 25, 30])
        y = numpy.array([0.003767, 0.005387, 0.007612, 0.01062, 0.014659, 0.019826, 0.027125]) #used to estimate maximum humidity ratio based on current temp
        pyplot.xlim(35)
        maxhumidratio = numpy.interp(weather_data['main']['temp'],x,y)
        if grasses == 1:
            runtime2 = ((0.623*area)+(25+19*weather_data['wind']['speed'])*area*(maxhumidratio-
                            maxhumidratio*.01*weather_data['main']['humidity']))/FlowRate #runtime calculations
        if grasses == 0:
            runtime2 = ((2*0.623 * area) + (25 + 19 * weather_data['wind']['speed']) * area * (maxhumidratio -
                            maxhumidratio * .01 * weather_data['main']['humidity'])) / FlowRate

        maxtime = (plantavail2[soils]*area*6 + ((25 + 19 * weather_data['wind']['speed']) * area * (maxhumidratio -
        maxhumidratio * .01 * weather_data['main']['humidity'])*infil2[soils]))/FlowRate #equation that calculated how much watering time is needed to saturate the soil
        runner = runtime2
        if runtime2 >= maxtime:
            runner = maxtime
        print(runtime2)
        iPktId[0] = 0x47000000 + len("ZONE 1 ACTIVE")
        port.write(struct.pack("i",iPktId))
        port.write("ZONE 1 ACTIVE")
        print(maxtime)

        i = 0
        if (not isDiqual(final_url)>0) and (alarm2 == 8 or runprof == 10):
            for x in gpios:
                statusstring = "ZONE " + i+1 + " ACTIVE"
                gpio.output(x, gpio.HIGH)
                if(i!=0):
                    statusstring = "ZONE "+i+" DEACTIVATED" + statusstring
                    gpio.output(gpios[i - 1], gpio.LOW) #light up respective LED
                iPktId[0] = 0x47000000 + len(statusstring)
                port.write(struct.pack("i", iPktId))
                port.write(statusstring)
                time.sleep(runner)
                runtime2 = runtime2 - maxtime
                i += 1
        if maxtime == 0:
            break
        if(ValBegHr+1<ValEndHr):
            ValBegHr+=1
        elif dayof<len(days):
            dayof+=1
        else:
            dayof=0
        val = 0
        time.sleep(5)

            
if __name__ == '__main__':
    main()
