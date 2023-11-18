from datetime import datetime

itstime = datetime.now()
date_time = itstime.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:", date_time)
daysetting = 0
lowertime = 0
uppertime = 0
print(itstime.strftime("%d"))
# Results in current date and time
if (itstime.strftime("%d") == '17'):
    print("water go!")
else:
    print("no water")