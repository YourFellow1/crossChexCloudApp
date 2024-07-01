from datetime import date, datetime, timedelta
import time
import util
from dateutil import parser
from logger_config import logger as logging
import globals
import os
import configparser

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
        print(timeformat, end='\r')
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