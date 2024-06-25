# Messages to not take up space?

#### Use this to configure different options. Report_length is const.
### Sites need updated.
## make sure site_names matches above.

#-----------Locked in reports-----------
# Report_length = selection of reports to run.
report_length = '''*************************************
select the report length you're looking for:
1. Today
2. Single day (select the day)
3. Two days
4. Past week (From today)
5. Enter date range
6. Past Month (select month)
7. Last badge by device.
*************************************\n'''
num_of_lengths = 7

# Months
months = '''***************************************
Select the month:
1. January
2. February
3. March
4. April
5. May
6. June
7. July
8. August
9. September
10. October
11. November
12. December
***********************************\n'''

#------------------- End of locked in messages --------

#-------------------------------------- Site Config -----
report_site = '''*************************************
Select your site:
1. All
2. TJX-Marshalls
3. Kiss
4. GMDR2
5. Partstown
6. Sanmar
7. Dollar General
8. Frito Whitestown
9. THM
10. Name not listed - Show all...
*************************************\n'''

site_names = {
    1: "All",
    2: "TJX-Marshalls",
    3: "Kiss",
    4: "GMDR2",
    5: "Partstown",
    6: "Sanmar",
    7: "Dollar General",
    8: "Frito Whitestown",
    9: "TMH",
    10: "Site Not Listed"
}

num_of_sites = 10 # The number of options in "Report_site

#---------------------------End Site Config

#-----------------Device Config
device_names = {
    "Partstown": 5,
    "GMDR2": 4,
    "Dollar General": 7,
    "TMH": 9,
    "TJX Marshalls": 2,
    "TJX Marshalls - OFFICE": 2,
    "Frito_Whitestown": 8,
    "Kiss_1": 3,
    "Sanmar_1": 6
}

#-------------End Device Config


select_date = "Please enter date (format = YYYY-MM-DD): "

select_start_date = "Please enter start date (format = YYYY-MM-DD): "
select_end_date = "Please enter end date (format = YYYY-MM-DD): "

select_month = "Please enter the month (format = MM)"
