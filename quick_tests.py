from datetime import date, timedelta, datetime
import times
import time
import util
import pytz

# # Think of the dates as an object.. because... they are.
# time1 = datetime.now()

# time2 = times.str_to_datetime('2024-07-02T09:52:36+00:00')
# print(f"time2: '{time2}' vs time1: '{time1}'")

# time3 = time1.replace(tzinfo=pytz.utc)
# time3_str = time3.isoformat(timespec='seconds')

# print(f"The string for time3 = {time3_str}")


# temp = times.minute_less()
# print("first reading")
# print(f"({temp[0]}, {temp[1]})")

# times.set_config_timestamp()
# print("modified the file")
# time.sleep(3)

# temp2 = times.minute_less()
# print("second reading")

# print(f"({temp2[0]}, {temp2[1]})")

# if temp2[0]:
#     print("60 seconds must pass between API requests")
#     times.countdown(temp2[1])

debounce = 30

# #Example including from iso - will NOT compare with the lower "datetime.now()"
# #Error is "can't subtract offset-naive and offset-aware datetimes."
# time1 = datetime.fromisoformat('2024-07-02T09:52:36+00:00')

# time.sleep(5)

# time2 = datetime.now()

#Now let's try taking the date TO isoformat and back (time2)
time1 = datetime.fromisoformat('2024-07-02T09:52:36+00:00')

time.sleep(5)

# Below is a no.. but I think I can make it work with tzinfo change.
# time2 = (datetime.fromisoformat(datetime.now().isoformat()))

# Yep. can we skip a step?
time2 = datetime.now()
time2tz = time2.replace(tzinfo=pytz.utc)
time3_str = time2tz.isoformat(timespec='seconds')
time3 = datetime.fromisoformat(time3_str)

# Again. yep. time4 compared no problem.
# So the fix to naieve-offset was the tz info. dumb.
# Now the question is if I change this in the 'within_debounce' function or the way we store.
time4 = time2.replace(tzinfo=pytz.utc)

print(times.within_debounce(time1, time4, debounce))

# devices = util.get_device_by_num(2)

# print(f"devices: {devices}")
