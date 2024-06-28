# Class for any and all API pulls.
# CrossChex Cloud
# THIS IS LOCAL TO THE CROSSCHEX APP PAGE.

import requests
from datetime import timedelta, date, datetime
import json
import math
import csv
import os

relative_path = "crossChex_App\API_KEY.csv"
url = "https://api.us.crosschexcloud.com"

#Successful for finding a nearby file. (Not good with OS.dir stuff yet)
def find_nearby_file(filename):
    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")
    
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isfile(item_path) and item == filename:
            print(f"Found file: {item_path}")
            return item_path
    
    print(f"File '{filename}' not found in the current directory.")
    return None

## for finding a folder in the root?
def find_file(root_folder, file_name):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None


# Getting the API key from a local file (csv).
def get_API_KEY():
    
    #Create dict for the key to be stored as a string.
    API_KEY = []
    

    # Get the API_KEY file.
    target_filename = "API_KEY.csv"
    root_folder = os.getcwd()
    try:
        filePath = find_file(root_folder, target_filename)
    except Exception as e:
        print(f"File '{target_filename}' not found: please try again.")
        input("Press enter to exit in disgrace")
    finally:
        if filePath:
            print(f"File '{target_filename}' found! Carry on.")
        else:
            print(f"File '{target_filename}' not found.")
            input("Press enter to exit: with a failure")
    
            
    # API_KEY.csv, getting the info from it, store under API_KEY[].
    with open(filePath, "r") as APIfile:
        reader = csv.reader(APIfile)
        for row in reader:
            value = row[0].strip()
            API_KEY.append(value)
    return API_KEY

# Set the time at JUST past midnight.
def begin_of_day(timestamp):
    # Keep it simple. Just go to 0's
    return timestamp.replace(hour=0, minute=0, second=0)
    
# Set the time at JUST before midnight.
def end_of_day(timestamp):
    # Keep it simple. Just go to last second of the day. 
    return timestamp.replace(hour=23, minute=59, second=59)


# Well, the filter list is pretty set. Don't need to touch in the refactoring.
def filter_list(page):
    compiled_list = []
    for name in page["payload"]["list"]:
            temp_list = []
            
            # Employee info - Sequence matters.
            emp = name.get("employee")
            temp_list.append(emp.get("last_name"))
            temp_list.append(emp.get("first_name"))
            temp_list.append(emp.get("workno"))

            # Device
            temp_list.append(name.get("device").get("name"))

            temp_time = datetime.fromisoformat(name.get("checktime")) - timedelta(hours=5)
            # temp_date = (str(temp_time.month) + "/" + str(temp_time.day) + "/" + str(temp_time.year))
            temp_date = (temp_time.strftime("%m/%d/%Y"))
            temp_minute = (temp_time.strftime("%H:%M:%S"))
            # Example: '2024-05-06T21:06:16+00:00'
            temp_list.append(temp_date)
            temp_list.append(temp_minute)

            # Add to formatted list
            compiled_list.append(temp_list)
    return compiled_list

class API:
    
    # const
    url = "https://api.us.crosschexcloud.com"

    # Everything needed for the data pull from the API.
    def __init__(self):


        # Default headerId
        self.headerId = 'f1becc28-ad01-b5b2-7cef-392eb1526f39'
        
        # Time is now
        self.timestamp = datetime.now()
        
        # Set the time defaults to midnight to midnight.
        self.begin_time = begin_of_day(self.timestamp) # Def above
        self.end_time = end_of_day(self.timestamp) # Def above

        # Current page number (for iteration)
        # Default num of records per page. 1
        self.cur_page = 1
        self.num_per_page = 1
        
        # Default workno = ''
        self.workno = ''


        #Token is mandatory, so it needs to be gotted first thing.
        self.token = self.pullToken(get_API_KEY())


    # FINAL - returns the token neeed for the detailed payload.
    def pullToken(self, API_KEY):
        # Request to get the token. API key based.
        payload={'header[nameSpace]': 'authorize.token',
                 'header[nameAction]': 'token',
                 'header[requestId]': str(self.headerId),
                 'header[timestamp]': str(self.timestamp),
                 'payload[api_key]': str(API_KEY[0]),
                 'payload[api_secret]': str(API_KEY[1])}

        # Response - Json - pull the token only.
        response = requests.request("POST", url, data=payload)
        response_json = json.loads(response.text)
        return response_json["payload"]["token"]


    # Input beginning time, and the ending time. Mostly used internally.
    # Return the overall dictionary? -> but only one?
    def get_single_request(self, begin_time, end_time):
        
        # Payload to just pull a single record.
        payload={'header[nameSpace]': 'attendance.record',
        'header[nameAction]': 'getrecord',
        'header[version]': '1.0',
        'header[requestId]': str(self.headerId),
        'header[timestamp]': str(self.timestamp),
        'authorize[type]': 'token',
        'authorize[token]': str(self.token),
        'payload[begin_time]': str(begin_time),
        'payload[end_time]': str(end_time),
        'payload[workno]': str(self.workno),
        'payload[order]': 'asc',
        'payload[page]': str(self.cur_page),
        'payload[per_page]': str(self.num_per_page)}

        response = requests.request("POST", url, data=payload)
        return json.loads(response.text)

    # Get a full list, and return the CSV list?
    # Unorganized data? so return as list of dictionaries? Would that overcomplicate?
    def get_full_list_by_start_stop(self, begin_time, end_time):

        csv_list = []

        self.begin_time = begin_time.replace(hour=0, minute=0, second=0)
        self.end_time = end_time.replace(hour=23, minute=59, second=59)

        # to pull more than one page of records.
        more_records = True
        while more_records:
            # Loop through and check for total records/amount per page < page number
            self.num_per_page = 100
            response = self.get_single_request(self.begin_time, self.end_time)
            pages = math.ceil(self.get_num_of_records(response) / self.num_per_page)
            
            # Check for the page num
            if pages == self.cur_page or self.cur_page == 50: # Hardcode an escape if it goes above 50.
                more_records = False

            print("We have pulled " + str(self.cur_page) + " page(s)")
            print("total records: " + str(self.get_num_of_records(response)))
            self.cur_page += 1
            
            #Aight. so filter_list returns a list. We want that list appended item by item.
            unfiltered_list = filter_list(response)
            for list in unfiltered_list:
                csv_list.append(list)

        return csv_list
        
    # what page number of the request
    def set_page_num(self, num):
        self.cur_page = num
    # for iteration purposes, just add one.
    def next_page(self):
        self.cur_page += 1

    # Change number of records per page.
    def set_per_page(self, num):
        self.num_per_page = num

    # Workno adjustments
    def clear_workno(self):
        self.workno = ''
    # Workno assign
    def set_workno(self, num):
        self.workno = num

    # Taking in the dictionary, this will give the number of records.
    def get_num_of_records(self, response):
        return int(response["payload"]["count"])

    def move_begin_time_back(self, num_days):
        self.begin_time -= timedelta(days=num_days)
    
    def set_begin_time(self, time):
        self.begin_time = begin_of_day(time)

    def set_end_time(self, time):
        self.end_time = end_of_day(time)