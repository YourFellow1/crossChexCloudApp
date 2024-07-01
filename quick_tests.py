from datetime import date, timedelta, datetime
import times
import time


temp = times.minute_less()
print("first reading")
print(f"({temp[0]}, {temp[1]})")

times.set_config_timestamp()
print("modified the file")
time.sleep(3)

temp2 = times.minute_less()
print("second reading")

print(f"({temp2[0]}, {temp2[1]})")

if temp2[0]:
    print("60 seconds must pass between API requests")
    times.countdown(temp2[1])
    

