from datetime import datetime
from machine import Timer

itstime = datetime.now()
date_time = itstime.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:", date_time)
day = (input('Enter the day: '))
time = (input('Enter the time: '))
# Results in current date and time
if itstime.strftime("%d") == day and itstime.strftime("%H") == time:
    print("water go!")
else:
    print("no water")

tommy = Timer()