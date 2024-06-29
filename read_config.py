### Finally some success. Now to incorporate and replace messgaes.
## This is how you'll be able to keep this relevant after you leave.
# This was also just an example. right? lol.

import configparser

import os

def read_config():
    # Create a configparser object
    config = configparser.ConfigParser()
    
    # read the configuration file
    # Working directory only points to test code. so use ABS path.
    path = os.path.abspath(__file__)
    file_director = os.path.dirname(path)
    config_file = os.path.join(file_director, "SMApp_config.ini")


    config.read(config_file)
    
    # Access values from the configuration file
    headerID = config.get('Report', 'headerid')
    timestamp = config.get('Report', 'timestamp')
    endTime = config.get('API', 'endtime')
    
    # Return a dictionary with retrieved values.
    ## I can work with a dictionary!!
    config_values = {
        'HeaderId': headerID,
        'TimeStamp': timestamp,
        'Report_End_Time': endTime,

    }
    return config_values

    
if __name__ == "__main__":
    try:
        ## call it
        config_data = read_config()
        
        # Print the values
        print(f"HeaderId = {config_data['HeaderId']}")
        # pprint(config_data)
        print(config_data)
    except Exception as e:
        print(e)
    else:
        print("SOMETHING")
