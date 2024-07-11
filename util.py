### Use this guy for any rando functions needed for frequent use.
### IE... getting names, numbers, from dict.

import time
from exception import NotInRange
import logging
import globals
from logging.handlers import RotatingFileHandler
import os
from messages import open_emergency, welcome_screen
from logger_config import logger as logging
import configparser
from datetime import datetime, date, timedelta
import times
import pytz


#------------- DEFs from MAIN start --------------------------

# Set up find file.
def find_file(root_folder, file_name):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None

# Function to ensure csv file directory exists, make it if not.
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.warning(f"file/directory: '{directory}' was not found, so it was created nearby!")
    else:
        logging.info(f"file/directory: '{directory}' was found, moving on.")

# Is this an emergency situation?
def get_emergency():
    while True:
        emergencyMessage = input(open_emergency).lower()
            
        if emergencyMessage == 'y':
            print("Confirmed, emergency. Calculating now...")
            logging.warning(f"User selected '{emergencyMessage}' (emergency situation). Processing only a list for today")
            return True
        
        elif emergencyMessage == 'n':
            print("Aight. Carry on.")
            logging.info(f"User selected '{emergencyMessage}', and was directed to the main menu")
            return False
        
        else:
            print("Please input 'y' for yes emergency or 'n' for no emergency.")

# Welcome Screen
def welcome_menu():
    input(welcome_screen)
    pass

# Need to get site from input. return device names [list]
def get_device_by_num(num):
    # take in the number and get the device name
    device_list = []
    for item, value in config_data['Devices'].items():
        if value == str(num):
            device_list.append(item)        
    return device_list

# Loop that can be used for any number input. (Int >0 only)
def get_num_selection(message, botRange, topRange, number_purpose):
    while True:
        try:
            response = int(input(message))
            
            # Evaluates true if not in the range provided. 
            if response > topRange or response < botRange:
                
                raise NotInRange
            else:
                # Log successful selection.
                logging.info(f"For {number_purpose}: User response is: {response}")
                
                # Return.
                return response
        except ValueError:
            print("Must be a number")
            
        except NotInRange:
            print("Number must be in the range of the prompt")

#------------- DEFs from MAIN end --------------------------

#-------------- Config read start -----------------

def read_config():
    # Create a configparser object
    config = configparser.ConfigParser()
    
    # read the configuration file
    # Working directory only points to test code. so use ABS path.
    # ^^ also important for distribution of the app.
    try:
        # Find file has the built-in "joins" function.
        config_path = find_file(globals.current_file_directory, 'SMApp_config.ini')
        if not config_path:
            logging.error("Configuration file not found")
            return None
        
        # Read
        logging.debug(f"Reading configuration file from {config_path}")
        config.read(config_path)
        
        config_values = {}
        
        # Dynamically read through all the sections and options.
        for section in config.sections():
            config_values[section] = {}
            for option in config.options(section):
                config_values[section][option] = config.get(section, option)
                
        return config_values
    
    except Exception as e:
        logging.error(f"An error occurred when trying to read the config file: {e}")


# To populate the message 
def site_message(config_values):
    
    first_line = '''
    ----Site Selection----
Select the site (and select 1 for site data from all sites)'''

    for item in config_values['Sites'].items():
        tempMessage = f"\n{int(item[0])} : {item[1]}"
        first_line += tempMessage
    
    first_line += "\n-------------------------\n"
    return first_line

# To populate the month message (this or past month)
def month_message(config_values):
    
    first_line = '''
    ------Month Selection-----
    Which month?'''
    
    for item in config_values['Month'].items():
        tempMessage = f"\n{int(item[0])} : {item[1]}"
        first_line += tempMessage
        
    first_line += "\n--------------------------\n"
    return first_line
    

# message for reports (use same structure as site_message)
def report_message(config_values):
    
    first_line = '''
    ------- Report Selection ---------
    Select the type of report
    (for "who's on site right now") - restart and select 'y' for emergency'''
    
    for item in config_values['Report'].items():
        tempMessage = f"\n{int(item[0])} : {item[1]}"
        first_line += tempMessage
        
    first_line += "\n------------------------------\n"
    return first_line    
    
    
#-------------- Config read end -----------------



#-------- filter and sort functions ----------- TODO: REDO AND BE MORE FLEXIBLE.

## List = [last name, first name, workno, device, timestamp]
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

            # LL: format with isoformat.
            temp_time = datetime.fromisoformat(name.get("checktime")) - timedelta(hours=4)
            # temp_date = (str(temp_time.month) + "/" + str(temp_time.day) + "/" + str(temp_time.year))
            tempTZ_datetime = temp_time.replace(tzinfo=pytz.utc)
            temp_datetime = tempTZ_datetime.isoformat(timespec='seconds')
            # temp_date = (temp_time.strftime("%m/%d/%Y"))
            # temp_minute = (temp_time.strftime("%H:%M:%S"))
            # Example: '2024-05-06T21:06:16+00:00'
            temp_list.append(temp_datetime)

            # Add to formatted list
            compiled_list.append(temp_list)
    return compiled_list

# Function to figure out who's on site.
def who_onsite(in_list, site):
    
    # The incoming list has already been filtered.
    # And this should be all from the same date.
    # need to see if people are clocked in or not
    # Separate all-purpose clock-in/out scenario?
    
    clock_in_list = clock_in(in_list, emergency=True, site=site)
    

    pass

def filter_by_site(list, site):
    devices = get_device_by_num(site)
    
    # By devices passed through in "site"
    device_sorted_list = []
    for list in list:
        if list[3].lower() in devices:
            device_sorted_list.append(list)
    
    return device_sorted_list
    
    pass

# Run through a raw list and see who is clocked-in.
# when working with EOD, emergency will be false.
def clock_in(raw_list, emergency, site):
    
    # Restart class
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #Raw list starts with: [last name, first name, workno, device, timestamp]
    # Assumptions:
    # anything in less than [# (20?)] seconds isn't a separate badge-out.
    debounce_seconds = 75
    # anything still clocked ini stays in for emergency.
    # anyone still clocked in @ time of report is "clocked-Out" on this list.

    # Sort by workno.
    sorted_list = sorted(raw_list, key=lambda x: x[2]) # COOL. THIS IS HOW YOU SORT BY NOT FIRST INDEX!

    device_sorted_list = filter_by_site(sorted_list, site)
    
    ## Go through each, and append(status).
    in_out_list = []
    last_employee = ''
    last_time = datetime.now()
    new_employee = False
    new_day = False
    within_debounce = False

    # '''If it's a new employee, clock in.
    # if it's same employee, new day, clock in.
    # if it's same employee, same day, within debounce - ignore.
    # if it's same employee, same day, outside debounce - change state (what about ignore?)
    
    
    # to check who's onsite:
    # list, same employee, last status for today.
    
    # To automatically clock out:
    
    # '''
    
    # Status options: in, out, ignore
    last_status = ''
    for list in device_sorted_list:
        #Compare times: True = Not a duplicate punch (outside the debounce time).
        # Compare dates first. date's the same, continue. If different...
        ####### Wait! compare one outcome at a time.
        if list[2] != last_employee:
            list.append('in')
            pass
        
        
        in_out_list.append(list)
        last_employee = list[2]
        last_time = list[5]
        last_status = list[6]
        
        
    if emergency:
        #TODO: evaluate each person, add to list to return.
        pass
    else:
        #TODO: evaluate each person, set final status?
        pass
    pass
#--------------- Filter and sort f(x) end -----------
# Create the input for site list.



##### Below was a test.. and it took me the better part of an hour to figure it out.
### please have this saved as an example to learn from!!!
config_data = read_config()

# site_message = site_message(config_data)

# print(site_message)

# API = config_data['API']

# print(API)
# site_message = {}
# for item in config_data['Sites'].items(): # .items will mean it comes as a tuple.
#     print(f"item: {item[0]} -> value: {item[1]}")


# # This is the structure for a TWO D loop through.
# for option, section in config_data.items():
#     for item, value in section.items():
#         print(f"({option}) -> ({item}) -> value: {value}")
# config_data = read_config()
# print(f"Len of config_data: {len(config_data)}")
# print(f"Len of config_data['sites']: {len(config_data['Sites'])}")