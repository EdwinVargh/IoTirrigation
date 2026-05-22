I made this project in the 11th grade for the class Interdisciplinary Study and Mentorship. Under the mentorship of an employee from Corning Optical Communications, I designed a system that calculated the runtime of sprinklers on a household lawn, using data referenced from the internet and a network of physical sensors. Although I tested only a prototype, my tests concluded that my system could reduce water use by up to 30% compared to traditional systems.

ADC.py --

Since the Raspberry Pi lacks a built-in ADC, this code approximates analog-to-digital readings from the sensors.
The code first establishes the I2C address as 0x48 and uses the System Management Bus as the communication channel.
The code then sets the bus to continuously sample the voltage and write the data to the conversion register.
The while loop reads in the data one byte at a time and prints the ADC reading.

RTC.py --

For the Raspberry Pi to keep track of time even when powered off, I attached an Adafruit PCF8563 real-time clock as a peripheral. This code was used to test the real-time clock.
The BCDtoDec_byte and DectoBCD_byte help to translate between the RTC's binary-coded decimal data and the binary data the computer expects to read.
The RTC is initialized and set up with an interrupt service routine that monitors GPIO 23, triggering a callback when it detects a falling edge.
The while loop reads data from the bus and triggers the interrupt callback function when the time reaches 5:00 PM.

algorithm.py --

Almost all of the logic is handled within the main function, except for some hardware helper functions, and the isDiqual function that detects whether the weather (fetched by an API call) is raining or the ground moisture levels are already too high to justify irrigation.
The system receives a packet of all the relevant information entered from the GUI by the user and collects weather data from the internet.
The data is then written to the Raspberry Pi over the serial port.
Using all of the information from the GUI and hardware readings, the system calculates the overall runtime, up to maxtime.
Finally, in the system's while loop, the system sets the timer and waits. Whenever the alarm is triggered (or the system is set to immediately run), the system activates each zone for the allotted runtime.

closest station.py -- 

This program finds the weather station that is closest to the user's latitude and longitude by finding the haversine distance of each weather station from Oracle Apex data.
This program was not utilized in the prototype.

fetchweather.py -- 

This program tests the API call that gets all the weather data from the internet.

guicode.py -- 

Based on the user's selections in the GUI, the system receives a packet containing all relevant information, including days of operation, lawn grass type, and runtime hours. 
Most of this code is also used in the main algorithm, though not called from this python file for reasons I don't remember.

haversine.py -- 

This code calculates the haversine distance between two points on Earth, accounting for Earth's curvature. This program is used to find the closes weather station to the user's latitude and longitude.

interrupt.py -- 

This program was written to test interrupts with the Real Time Clock, using a lot of the same features outlined in RTC.py.

moist.py -- 

systemtest1.py -- 
