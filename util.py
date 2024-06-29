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
            emergency = True
            break
        elif emergencyMessage == 'n':
            print("Aight. Carry on.")
            logging.info(f"User selected '{emergencyMessage}', and was directed to the main menu")
            emergency = False
            break
        else:
            print("Please input 'y' for yes emergency or 'n' for no emergency.")

# Welcome Screen
def welcome_menu():
    input(welcome_screen)
    pass

# Need to get site from input. Return number.
def get_site_input_num():
    pass

# Loop that can be used for any number input. (Int >0 only)
def get_num_selection(message, botRange, topRange, number_purpose):
    while True:
        try:
            response = int(input(message))
            if response > topRange or response < botRange:
                
                raise NotInRange
            else:
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

# Def for using config file... didn't use.
def use_config_read():
    config_data = read_config()
    print(config_data['API'])

# To populate the message 
def site_message(config_values):
    
    first_line = '''----Site Selection----
Select the site (and select 1 for site data from all sites)'''

    for item in config_values['Sites'].items():
        tempMessage = f"\n{int(item[0])} : {item[1]}"
        first_line += tempMessage
    
    first_line += "\n-------------------------"
    return first_line
#-------------- Config read end -----------------

# Create the input for site list.



##### Below was a test.. and it took me the better part of an hour to figure it out.
### please have this saved as an example to learn from!!!
# config_data = read_config()

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
config_data = read_config()
print(f"Len of config_data: {len(config_data)}")
print(f"Len of config_data['sites']: {len(config_data['Sites'])}")