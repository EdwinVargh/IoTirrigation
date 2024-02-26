import smbus2
import time


def main():
    RtcI2cAddr = 0x68
    bus = smbus2.SMBus(1)

    bus.write_byte_data(RtcI2cAddr, 0x00, 0x08)
    bus.write_byte_data(RtcI2cAddr, 0x01, 0x00)

    myTime = [0x0, 0x59, 0x24, 0x11, 0x01, 0x05, 0x64]
    bus.write_i2c_block_data(RtcI2cAddr, 0x03, myTime)

    myTime2 = [0x0, 0x25, 0x80, 0x80]
    bus.write_i2c_block_data(RtcI2cAddr, 0x0A, myTime2)

    while(True):
        time.sleep(0.5)
        val = bus.read_byte_data(RtcI2cAddr, 0x01)
        print("Alarm value "+val)


if __name__ == '__main__':
    main()