file = "C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\Week starting_05_21---05_28_2024-16_54.csv"
file2 = "C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\past_fortnight---05_23_2024-10_39.csv"
file3 = "C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\Today---05_29_2024-22_26.csv"
import csv
import os
from pprint import pprint
import messages
from datetime import date, timedelta, datetime


#--------Functions for the page
# device name to site. Not report.site (that's a num).
# Refactor. Need to go from site num to site and vice versa.
def site_by_device(device):
    if device == "TJX Marshalls" or device == "TJX Marshalls - OFFICE":
        return "TJX Marshalls"
    else:
        return device

# Pass in the site number, and it spits out site Name.
def site_num_to_name(num):
    dict = messages.site_names
    return dict[num]

# Pass in the device (from API data), and it spits out site num
def site_device_to_num(device):
    dict = messages.device_names
    return dict[device]

# Pass in the num to get the device?
# Technically returns a tuple if there's more than one device/site
def site_num_to_device(num):
    dict = messages.device_names
    keys = [key for key, value in dict.items() if value == num]
    return keys

# Returns the abs value of TIME difference of two times (Date object)
def time_difference(time1, time2):
    first = datetime.strptime(time1, "%H:%M:%S")
    second = datetime.strptime(time2, "%H:%M:%S")
    return abs(first - second)

# This will run for all sites, or one site. Depends on list passed in.
# MUST be sorted list to work right. [person name, workno, device, date, time]
def assign_in_out(list):
    inOut = []
    remember = ['', '', '','','','']
    for sub_list in list:
        
        # logic: if same name, same place (either of the sites), same day, different time, then it changes.
        
        if remember[1] != sub_list[1]:
            # Not same person. Immediate "in"
            sub_list.append('Clock-In')
        
        elif site_by_device(remember[2]) != site_by_device(sub_list[2]):
            # same person, not same site. Immediate "in"
            sub_list.append('Clock-In')
        
        elif remember[3] != sub_list[3]:
            # Same person, same site, not same date. Immediate "in"
            sub_list.append('Clock-In')
            # Here is where we check for a lack of clock-out?
            # No. need to further check if they were out before.
            if remember[5] == "Clock-In":
                print(str(sub_list[0]) + " DID NOT BADGE-OUT ON " + str(sub_list[3]))
        
        elif time_difference(remember[4], sub_list[4]) < timedelta(minutes=2):
            # same person, same site, same date, less than 2 min apart.
            # Change the time for testing purposes.
            sub_list.append('Clock-In')
        
        elif remember[5] == 'Clock-Out':
            # If the previous was false, then it's True next.
            sub_list.append('Clock-In')
        
        else:
            # After all potential 'in's are covered, out is the remainder.
            sub_list.append('Clock-Out')

        # What do we do with sub_list?
        inOut.append(sub_list)
        remember = sub_list
    
    # Return the list with 'True' for clock-in. False for clock-out.
    return inOut

# Take the in_out list (After calling assign_in_out) and say who's onsite today.
# this will list of who has been onsite today. # Write a seperate for current_onsite.
def who_on_site_today(list, siteNum): # This use of site is by the device name...
    today_site = []

    # Establish datetime for comparison to the list.
    today = datetime.now().strftime("%m/%d/%Y")

    # Remember = comparison for next one. Just need person and in/out.
    remember = ['workno','clock-in status']

    # Loop through all.
    for sub_list in list:

        # Check site first.
        if site_device_to_num(sub_list[2]) == siteNum:
            print("we're running just one?")
            # Check for today (the yes will be onsite and today.)
            if sub_list[3] == today:
                
                # Unique names (workno). Print out names, though.. Add to today_site.
                if remember[0] != sub_list[1]:
                    today_site.append(sub_list[0])
        remember = [sub_list[1], sub_list[5]]
    return today_site

#-----------End of scratch functions

#------- Main run.



# #all code below doesn't run when crossChex_App.py runs.
# workingList = []
# with open(file3, "r") as testFile:
#     reader = csv.reader(testFile)
#     for row in reader:
#         workingList.append(row)

# sorted_list = sorted(workingList, key=lambda x: x[2]) # COOL. THIS IS HOW YOU SORT BY NOT FIRST INDEX!

# # pprint(sorted_list)
# idList = []
# for list in sorted_list:
#     if list[3] == "TJX Marshalls" or list[3] == "TJX Marshalls - OFFICE":
#         idList.append([(str(list[1]) + " " + str(list[0])),list[2], list[3], list[4], list[5]])

# # pprint(idList)



# # for counter
# # list.insert(index, value)


# inOutList = assign_in_out(idList)

# onsiteToday = who_on_site_today(inOutList, "TJX Marshalls")

# print(onsiteToday)


print(site_num_to_name(2))