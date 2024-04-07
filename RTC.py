import smbus
import time
import RPi.GPIO as gpio

# RTC is on I2C channel 1
bus = smbus.SMBus(1)
# AdaFruit RTC is hardwired to address 0x68
RtcI2cAddr = 0x68
# Alarm "do not use" register val (disables that paramters alarm)
ALARMDONOTUSE = 80
DaysofWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


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


def rtc_alarm_callback(channel):
    # Clear Alarm in Control Register 2
    bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
    # Set the Alarm on RTC to Monday at 17:01 24hr time (5:01 PM)
    print("RTC Alarm Triggered")
    Mytime = rtc_GetTime()
    print("Current time is", DaysofWeek[Mytime[0]], " ", Mytime[4], ":", Mytime[5], ":", Mytime[6])


def rtc_set_datetime(Wkday, months, Mthday, years, hours, minutes, seconds):
    MyTime = [DectoBCD_byte(seconds), DectoBCD_byte(minutes), DectoBCD_byte(hours), DectoBCD_byte(Mthday),
              DectoBCD_byte(Wkday), DectoBCD_byte(months), DectoBCD_byte(years)]
    bus.write_i2c_block_data(RtcI2cAddr, 0x03, MyTime)


def rtc_GetTime():
    MyTime = bus.read_i2c_block_data(RtcI2cAddr, 0x03)
    RtnTime = [BCDtoDec_byte(MyTime[4]), BCDtoDec_byte(MyTime[5]), BCDtoDec_byte(MyTime[3]), BCDtoDec_byte(MyTime[6]),
               BCDtoDec_byte(MyTime[2]), BCDtoDec_byte(MyTime[1]), BCDtoDec_byte(MyTime[0])]
    return RtnTime


def rtc_set_alarm_datetime(Wkday, hour, minute, Mthday, years):
    MyTime = [DectoBCD_byte(Wkday), DectoBCD_byte(hour), DectoBCD_byte(Mthday), DectoBCD_byte(years)]
    bus.write_i2c_block_data(RtcI2cAddr, 0x0A, MyTime)


def main():
    # RTCs Alarm pin is connected to GPIO 23
    RtcAlrmPin = 23
    InitRtcWithIrq(RtcAlrmPin)
    # Set the time and date on RTC to Monday, May 11, 1964 @ 16:59:00 24hr time (4:59 PM)
    rtc_set_datetime(1, 5, 11, 64, 16, 59, 0)
    # Set the Alarm on RTC to Monday @ 17:00 24hr time(5:00 pm)
    # Enable RTC Alarm
    bus.write_byte_data(RtcI2cAddr, 0x00, 0x02)

    while (True):
        time.sleep(0.5)
        Alrm = bus.read_byte_data(RtcI2cAddr, 0x01)
        PinVal = gpio.input(RtcAlrmPin)
        print("Alrm Reg: ", Alrm, "Pin: ", PinVal)


#        Mytime = rtc_GetTime()
#        print("Current time is", DaysofWeek[Mytime[0]], " ", Mytime[4],":",Mytime[5],":",Mytime[6])


if __name__ == "__main__":
    main()
