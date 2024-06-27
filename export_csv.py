# How we want to export the CSV.
# Using this for all the record keeping.

import csv
import os
from datetime import datetime, date, timedelta

import os
import csv


## Let's expand this to use the find_file? Then we can start printing to a computer again.
# This makes me feel like I need to start all over again...

class CSV_EXPORT:
    
    def __init__(self, list, purpose):
        # Set up some properties
        self.purpose = purpose

        # This updates the filename, and includes the path. Hmm...
        # Adjusted to not include folderpath.
        # Pretty sure this isn't the purpose of classes. :0
        self.fileName = self.fileName_from_purpose()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_path = os.path.join(self.script_dir, self.fileName)

        self.target_dir = os.path.dirname(self.relative_path)
        
        print("And target_dir: " + str(self.target_dir))



        self.list = list



    def fileName_from_purpose(self):
        self.fileName = str(self.purpose) + "---" + str(datetime.now().strftime("%m_%d_%Y-%H_%M")) + ".csv"
        return self.fileName
    
    def print_to_file(self):

        # Check for target_dir and make if not there. 
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        
        # Print the contents to a file. No matter what was pulled.

        with open(self.relative_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.list:
                writer.writerow(row)
        print(f"CSV file saved to {self.relative_path}")




''' -----Pulled from the effective API_PULL.PY example.
--- keep getting an error for 
"an error occurred and now we know where to start: [Errno 2] No such file or directory: 'C:\\Users\\jfellow\\AppData\\Local\\Temp\\_MEI231162\\csv\\Today---05_30_2024-22_23.csv'"
def find_nearby_file(filename):
    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")
    for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)
            if os.path.isfile(item_path) and item == filename:
                print(f"Found file: {item_path}")
                return item_path

'''