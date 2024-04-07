import serial
import time
import struct
from smbus2 import SMBus, i2c_msg

# HiLetgo ADC is hardwired to address 0x48
AdcI2cAddr = 0x48
# Address Pointer Register addresses
AdcConvReg = 0x00
AdcCfgReg = 0x01
AdcCompLoReg = 0x02
AdcCompHiReg = 0x03


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


def main():
    HdrLen = 4

    port = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, timeout=1.0)
    InitMoistureAdc()

    while (True):
        MoistureVolts = ReadMoistureAdc()
        fdata = struct.pack("f", MoistureVolts)
        port.write(fdata)
        time.sleep(0.2)

        num_bytes = port.inWaiting()
        if num_bytes >= HdrLen:
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
                    SunValid = (ValidDays >> 6) & 0x01
                    MonValid = (ValidDays >> 5) & 0x01
                    TueValid = (ValidDays >> 4) & 0x01
                    WedValid = (ValidDays >> 3) & 0x01
                    ThuValid = (ValidDays >> 2) & 0x01
                    FriValid = (ValidDays >> 1) & 0x01
                    SatValid = ValidDays & 0x01
                    ValBegHr = ord((struct.unpack_from('c', rx_data, offset=5))[0])
                    ValBegMin = ord((struct.unpack_from('c', rx_data, offset=6))[0])
                    ValBegAmPm = ord((struct.unpack_from('c', rx_data, offset=7))[0])
                    ValEndHr = ord((struct.unpack_from('c', rx_data, offset=8))[0])
                    ValEndMin = ord((struct.unpack_from('c', rx_data, offset=9))[0])
                    ValEndAmPm = ord((struct.unpack_from('c', rx_data, offset=10))[0])
                    Zone = ord((struct.unpack_from('c', rx_data, offset=11))[0])
                    Zone1Grass = (Zone >> 4) & 0x0F
                    Zone1Soil = Zone & 0x0F
                    Zone = ord((struct.unpack_from('c', rx_data, offset=12))[0])
                    Zone2Grass = (Zone >> 4) & 0x0F
                    Zone2Soil = Zone & 0x0F
                    Zone = ord((struct.unpack_from('c', rx_data, offset=13))[0])
                    Zone3Grass = (Zone >> 4) & 0x0F
                    Zone3Soil = Zone & 0x0F
                    Zone = ord((struct.unpack_from('c', rx_data, offset=14))[0])
                    Zone4Grass = (Zone >> 4) & 0x0F
                    Zone4Soil = Zone & 0x0F
                    Zone = ord((struct.unpack_from('c', rx_data, offset=15))[0])
                    Zone5Grass = (Zone >> 4) & 0x0F
                    Zone5Soil = Zone & 0x0F
                    print("FlowRate = ", round(FlowRate, 2), " Begin Hr ", ValBegHr, ":", ValBegMin, ":", ValBegAmPm,
                          " End Hr ", ValEndHr, ":", ValEndMin, ":", ValEndAmPm, sep='')
                    print("Sunday ", SunValid, " Monday ", MonValid, " Tuesday ", TueValid, " Wednesday ", WedValid,
                          " Thursday ", ThuValid, " Friday ", FriValid, " Saturday ", SatValid, sep='')
                    print("Zone1 ", Zone1Grass, ":", Zone1Soil, " Zone2 = ", Zone2Grass, ":", Zone2Soil, sep='')

            elif ((iPktId[0] & 0xFF000000) == 0x77000000):
                PktLen = ((iPktId[0] & 0x000000FF) - HdrLen)
                time.sleep(0.5)
                num_bytes = port.inWaiting()
                if (num_bytes < PktLen):
                    print("Expected ", PktLen, "bytes on serial port, only received ", num_bytes)
                    break
                else:
                    rx_data = port.read(PktLen)
                    fdata = struct.unpack_from('f', rx_data, offset=0)
                    print("Manual Temperature = ", round(fdata[0], 2))
                    fdata = struct.unpack_from('f', rx_data, offset=4)
                    print("Manual Humidity = ", round(fdata[0], 2))
                    fdata = struct.unpack_from('f', rx_data, offset=8)
                    print("Manual Wind Speed = ", round(fdata[0], 2))

    port.close()


if __name__ == "__main__":
    main()
