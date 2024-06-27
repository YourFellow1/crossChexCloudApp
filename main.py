### = Explaining thought process. (Joey Specific notes)
# = explaining a program step.


### Restart 6_26. Time to treat the rest like practice.
### it WAS a learning experience. Now to make it fucking happen.

import os
import logging
from logging.handlers import RotatingFileHandler
import signal
import messages

#Set main path and directory
# C:\Users\jfellow\OneDrive - Bastian Solutions\TestCode\Python\crossChex_App\main.py
current_file_path = os.path.abspath(__file__)
# C:\Users\jfellow\OneDrive - Bastian Solutions\TestCode\Python\crossChex_App
current_file_directory = os.path.dirname(current_file_path) 
logFilePath = os.path.join(current_file_directory, 'crossChexLog.log')


#--------- LOGGER SETUP -------------------------
# Config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rotating = 10MB files, keeps the last 5. 
handler = RotatingFileHandler(logFilePath, maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.INFO)

# Configure logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to the root logger
logging.getLogger().addHandler(handler)

#------------- END LOGGER SETUP. -----------------------

# Running logic
running = True

def signal_handler(sig, frame):
    global running
    print("Signal received, exiting gracefully...")
    logging.info('Selected to close via ctrl + c')
    running = False

# Signal handler - for Ctrl+c to give a specific response.
signal.signal(signal.SIGINT, signal_handler)

# Set up find file.
def find_file(root_folder, file_name):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None

# Function to ensure csv file directory exists, make it if not.
### including logging for my benefit.
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.warning(f"file/directory: '{directory}' was not found, so it was created nearby!")
    else:
        logging.info(f"file/directory: '{directory}' was found, moving on.")

# Loop counter for main loop.
mainLoopCounter = 0        

def main():

    # Overall try/catch
    try:
        # Make sure the directory for the CSV files exists.
        csv_directory = 'historical csv files'
        ensure_directory_exists(csv_directory)
        
        while running:
            mainLoopCounter += 1
            logging.info(f"Entering loop # {mainLoopCounter}")
            
            
            
            
    
    except Exception as e:
        logging.critical(f"Program closed when it wasn't supposed to. Error: {e}")
        print(f"critical error: Program closed when it wasn't supposed to. Error: {e}")
        
        ### Use an input to manually close the program after failure.
        input("Press Enter to Exit... (disgracefully)")
        
    else:
        logging.info("Successful completion of the program. Looping back around")
        
        ### Use an input ot manually close go back to the front of the loop.
        input(messages.loop_program_message)
