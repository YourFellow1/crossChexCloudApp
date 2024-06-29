import configparser
import globals
from datetime import date, datetime, time, timedelta
import os

configFilePath = FilePath = os.path.join(globals.current_file_directory, 'SMApp_config.ini')

def create_config():
    config = configparser.ConfigParser()
    getTimestamp = datetime.now()
    # Add sections and key-value pairs
    config['Report'] = {'headerId': '123456', 'timestamp': getTimestamp}
    config['API'] = {'beginTime': getTimestamp, 'endTime': (getTimestamp + timedelta(days=1))}
    
    
    # Write to a file
    with open(configFilePath, 'w') as configfile:
        config.write(configfile)
    
if __name__ == "__main__":
    create_config()