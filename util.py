### Use this guy for any rando functions needed for frequent use.
### IE... getting names, numbers, from dict.

import time
from exception import NotInRange
import logging
import main
from logging.handlers import RotatingFileHandler
import os
import messages
from logger_config import logger as logging


# #--------- LOGGER SETUP -------------------------
# # Config
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# #--------- LOGGER SETUP -------------------------
# # Config
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # Rotating = 10MB files, keeps the last 5. 
# handler = RotatingFileHandler(main.logFilePath, maxBytes=10*1024*1024, backupCount=5)
# handler.setLevel(logging.INFO)

# # Configure logging format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # Add handler to the root logger
# logging.getLogger().addHandler(handler)

# # Logging in.
# logging.info("User opened the program, and logging has initiated - Currently in testing mode.")

# #------------- END LOGGER SETUP. -----------------------

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
        emergencyMessage = input(messages.open_emergency).lower()
            
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
    input(messages.welcome_screen)
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

# Used to validate int input of a dict/list.
### Pass in the use case? for exception/logging reasons?