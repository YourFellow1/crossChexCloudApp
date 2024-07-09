from datetime import date, datetime, timedelta
import time
import util
from dateutil import parser
from logger_config import logger as logging
import globals
import os
import configparser
import math

# Need to compare times, less than minute Return tuple of (Needs a timer BOOL, int of seconds?)
def minute_less():
    
    begin = get_config_timestamp()
    
    timedelta = datetime.now() - begin
    
    # Check for the seconds of timedelta and compare to minute.
    if time_in_seconds(timedelta) < 60:
        return (True, int(60 - (time_in_seconds(timedelta))))
    else:
        return (False, 0)

# Pass in a timedelta (literally) and spit out an int of seconds.
def time_in_seconds(timedelta):
    
    # Need to convert to seconds and export.
    return int(timedelta.days * 24 * 3600 + timedelta.seconds)
    
# Need to start a timer? this could be fun to learn.
def countdown(seconds):
    minutes = 0
    while seconds > 0:
        timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
        print("Time Remaining: " + timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print("Moving on!")

# pull config_data exactly now. just timestamp    
def get_config_timestamp():
    
    # Get config (use util)
    config_file = util.read_config()
    
    # Comes as a string - parse it to datetime.
    str_timestamp = config_file['Data']['last_request']
    timestamp = parser.parse(str_timestamp)
    
    return timestamp


# Write new timestamp to config file
# make sure to call this in MAIN!!
def set_config_timestamp():
    right_now = datetime.now()
    try:
        write_config_time(datetime.now())
        logging.info(f"sucessfully wrote the new timestamp {right_now}")
    except Exception as e:
        logging.info(f"Failed at set_config_timestamp: {e}")
        
def write_config_time(timestamp):
    # First, get the config_data.
    config_file = os.path.join(globals.current_file_directory, 'SMApp_config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Check for its existence before modifying (good call ducky)
    if 'Data' in config and 'last_request' in config['Data']:
        # modify the value
        config['Data']['last_request'] = str(timestamp)
        logging.info("able to find and change the value")
    else:
        logging.warning("Section 'Data' or key 'last_request' not found in the config file")

    # Now write the updated configuration back to the file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    logging.info("successfully wrote in timestamp")

# take in two times, if time1 is within debounce of time2 
# Return TRUE it it's within the parameter of debounce.
def within_debounce(time1, time2, debounce):
    
    # DOES matter which time is which
    timedelta = time2 - time1
    
    print(f"Time Delta: {timedelta}")
    if int(timedelta.seconds) < debounce:
        return True
    return False

# Take a string and make it work as datetime.
def str_to_datetime(str):
    # 2024-07-02 17:14:23,720
    # '2024-07-02T09:52:36+00:00' <- from the post request.
    
    time1 = datetime.fromisoformat(str)
    
    return time1

def dt_to_string(dt):
    
    time1 = dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    return time1