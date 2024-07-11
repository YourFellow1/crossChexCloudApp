## Example to save a list.
import pickle
import csv

# Run this first section one time. then just the last to retrieve.

# #----------------- CREATE PICKLE FILE WITH CSV ---------------

# my_list = []

# csv_file = 'C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\Week starting_05_24---05_31_2024-10_11.csv'

# with open(csv_file, newline='') as csvfile:
#     csvreader = csv.reader(csvfile)
    
#     for row in csvreader:
#         my_list.append(row)

# pickle_file = 'my_list.pkl'

# with open(pickle_file, 'wb') as file:
#     pickle.dump(my_list, file)

# #--------------- PICKLE JAR COMPLETE ---------------------
pickle_file = 'C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\test_data.pkl'


with open(pickle_file, 'rb') as file:
    my_list = pickle.load(file)

print(my_list)


