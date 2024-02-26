from smbus2 import SMBus, i2c_msg
import time


def main():
    AdcI2cAddr = 0x48

    AdcConvReg = 0x00
    AdcCfgReg = 0x01
    AdcCompLoReg = 0x02
    AdcCompHiReg = 0x03
    bus = SMBus(1)

    AdcConfig=[0x42,0x00]
    bus.write_i2c_block_data(AdcI2cAddr,AdcCfgReg,AdcConfig)
    bus.write_byte(AdcI2cAddr,AdcConvReg)

    Msg = i2c_msg.read(AdcI2cAddr, 2)

    while(True):
        time.sleep(0.5)
        bus.i2c_rdwr(Msg)
        b = list(Msg)
        val = b[0]*256+b[1]
        print(val*.000127, "volts of output")

if __name__ == '__main__':
    main()