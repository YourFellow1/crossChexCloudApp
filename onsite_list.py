# This is used for the algorithms to see who is currently onsite.


# Import Pandas to use the DataFrame.query functionality.
import pandas as pd


df = pd.read_csv('C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\api_work\\Latest_Data\\05_11_2024 14_17.csv')

unique_values = df.groupby('device')[df.columns[2]].unique().sort_index()
print(unique_values) # This printed a list of devices, with work no's associated.
# result = df.query("device == 'TJX Marshalls'")
# print(result)

#TODO: List of unique individuals, plus suspected of being gone and when.
