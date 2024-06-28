# not very pythonic... but sue me. Global variables for all classes.

import os


#Set main path and directory
# C:\Users\jfellow\OneDrive - Bastian Solutions\TestCode\Python\crossChex_App\main.py
current_file_path = os.path.abspath(__file__)
# C:\Users\jfellow\OneDrive - Bastian Solutions\TestCode\Python\crossChex_App
current_file_directory = os.path.dirname(current_file_path) 
logFilePath = os.path.join(current_file_directory, 'SMApp_ABI_Reporting.log')