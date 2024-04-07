import time
import RPi.GPIO as gpio
from smbus2 import SMBus, i2c_msg

def rtc_alarm_callback(channel):
    print("RTC Alarm Triggered")


def main():
    # AdaFruit RTC is hardwired to address 0x68
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

    # Configure gpio pin to interrupt on alarm
    gpio.setup(RtcAlrmPin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(RtcAlrmPin, gpio.FALLING, callback=rtc_alarm_callback)

    # Set the time and date on RTC to Monday, May 11, 1964 @ 4:59:00PM
    MyTime = [0x0, 0x59, 0x24, 0x11, 0x01, 0x05, 0x64]
    bus.write_i2c_block_data(RtcI2cAddr, 0x03, MyTime)

    # Set the Alarm on RTC to Monday, May 11, 1964 @ 5:00PM
    MyTime2 = [0x00, 0x25, 0x11, 0x80]
    bus.write_i2c_block_data(RtcI2cAddr, 0x0A, MyTime2)

    # Disable CLKOUT so it doesn't drive /INT1 pin
    bus.write_byte_data(RtcI2cAddr, 0x0F, 0x38)

    # Enable RTC Alarm
    bus.write_byte_data(RtcI2cAddr, 0x00, 0x0A)
    val = 0
    val2 = 0
    while (True):
        time.sleep(0.5)
        val = bus.read_byte_data(RtcI2cAddr, 0x01)
        val2 = gpio.input(RtcAlrmPin)
        if val2 == gpio.LOW:
            bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)
        print("Alrm Reg: ", val, "Pin: ", val2)


if __name__ == "__main__":
    main()