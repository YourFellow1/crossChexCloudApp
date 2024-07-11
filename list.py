import pickle

pick_file = 'C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\my_list.pkl'
with open(pick_file, 'rb') as file:
    my_list = pickle.load(file)

print(my_list)