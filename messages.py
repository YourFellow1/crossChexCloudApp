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

#---------------- INPUTS
select_date = "Please enter date (format = YYYY-MM-DD): "

select_start_date = "Please enter start date (format = YYYY-MM-DD): "
select_end_date = "Please enter end date (format = YYYY-MM-DD): "

select_month = "Please enter the month (format = MM)"

loop_program_message = '''*****************************************
Thank you for choosing SMApp for all (most) of your ABI needs.
We understand you have many options in resources for reporting on Contractor Hours,
and we thank you for your patronage.
Type 'Exit' and press the Enter Key to quit the program, or press just the Enter Key
to loop back around to the main menu.

******************************************************
'''

welcome_screen = '''SMAPP-SMAPP-SMAPP-SMAPP-SMAPP-SMAPP

Welcome to SMApp, ABI reporting edition
Please press enter to continue on to the main menu.

SMAPP-SMAPP-SMAPP-SMAPP-SMAPP-SMAPP
'''

open_emergency = '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Is this an emergency situation where you need a direct list of who's badged-in?
(y/n):'''

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
10. Name not listed - Show all...\n'''