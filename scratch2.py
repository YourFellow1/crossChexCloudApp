import csv
import os
from datetime import timedelta, date, datetime

import math
import json

# Original find file. all relative?
def find_nearby_file(filename):
    current_directory = os.getcwd()
    print(f"current directory: {current_directory}")
    
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isfile(item_path) and item == filename:
            print(f"Found File: {item_path}")
            return item_path
        
# Is there a way to search each file? Until all children are complete?
#Rubber ducky says, yes. Below is AI Generated. Works better...
def find_file(root_folder, file_name):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None
        
## Example usage
root_folder = os.getcwd()
print(root_folder)
## ^^ is back a couple folders, and it still runs.
file_name = "API_KEY.csv"

file_path = find_file(root_folder, file_name)

if file_path:
    print(f"File found: {file_path}")
    input("Press enter to exit...(successfully)")
else:
    print(f"File '{file_name}' not found in '{root_folder}'")
    input("press enter to exit.. (As a failure)")

# try:
#     find_nearby_file(target_file_name)
    
# except Exception as e:
#     print(f" The exception found == {e}")
#     input("press enter to exit... (in disgrace)")
# else:
#     input("Press Enter to exit... (successfully)")
