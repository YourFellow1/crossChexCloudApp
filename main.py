### = Explaining thought process. (Joey Specific notes)
# = explaining a program step.


### Restart 6_26. Time to treat the rest like practice.
### it WAS a learning experience. Now to make it fucking happen.

import os
import logging
from logging.handlers import RotatingFileHandler
import signal
import messages
import util
import api
from api import API, begin_of_day, end_of_day
import times
from logger_config import logger as logging
import sys
from datetime import datetime, date, timedelta
import csv
import pickle





# Running logic
running = True

def signal_handler(sig, frame):
    global running
    print("Signal received, exiting gracefully...")
    logging.info('Selected to close via ctrl + c')
    running = False

# Signal handler - for Ctrl+c to give a specific response.
signal.signal(signal.SIGINT, signal_handler)

# Loop counter for main loop.
## Not necessary, but something I will track during debugging.

mainLoopCounter = 0
emergency = False    
site_config = util.read_config()
num_of_sites = len(site_config['Sites']) # Includes "all" sites as #1
report_type = len(site_config['Report']) # includes 


def main():
    global mainLoopCounter
    global emergency
    global site_config # All the configuration data. Not just site.
    global num_of_sites
    # Overall try/catch
    try:
        # Make sure the directory for the CSV files exists.
        csv_directory = 'historical csv files'
        util.ensure_directory_exists(csv_directory)
        
        # TODO: Check past month.
        # TODO: Initialize most recent month.
        
        while running:
            mainLoopCounter += 1
            logging.info(f"Entering loop # {mainLoopCounter}")
            
            
            # Welcome message 
            util.welcome_menu()
            
# ---------- Get Site ------------------#
            ## site_config was initialized up top.
            # Call site_message
            site_message = util.site_message(site_config)
            # Get user input for site selection number
            site = util.get_num_selection(site_message, 1, len(site_config['Sites']), 'Which site?')
            
            # Check for an emergency situation.
            emergency = util.get_emergency()
            
            # Check if it's been a minute since last API request?
            must_countdown = times.minute_less()
            
            if must_countdown[0]:
                print("60 seconds hasn't elapsed since the last API request")
                print("60 seconds MUST elapse between requests")
                times.countdown(must_countdown[1]) # <- Ends with moving on message.
            
            # New instance of API with all defaults.
            new_api = API()
            
            data_type = 1 # default for EOD.
            
            # variable to capture all of it.
            full_list = []
            
            if not emergency:
                # Generate message: 
                report_message = util.report_message(site_config)
                
                # Get the num to work with.
                data_type = util.get_num_selection(report_message, 1, len(site_config['Report']), 'Checking Data_type')

                # react to data_type. (only here after validated selection)
                if data_type == 1:
                    
                    # Then we're working with an EOD report. so dates are still today.
                    # This is for the DSR - and what would we want that to execute?
                    # For now, we're not looking at the historical data. That would be a sweeping change.
                    # The difference would be the filter to clock everyone out today?
                    
                    pass
                elif data_type == 2:
                    
                    # This is the month boy. so we'll also want the hours, right? by group?
                    # or just a fulll ist of all transactions? TBD.
                    month_message = util.month_message(site_config)
                    month_type = util.get_num_selection(month_message, 1, len(site_config['Month']), 'This month or last')
                    
                    if month_type == 1:
                        # This month
                        new_api.set_to_this_month()
                        
                    elif month_type == 2:
                        # Last month
                        new_api.set_to_last_month()
                        

                elif data_type == 3:
                    
                    # It just now occurs to me that this isn't report type, but report time....
                    # Date Range for this one. so we need a way to input dates?
                    
                    pass
            
            # Run the range? If emergency, too, right? Get all raw data.
            
            raw_list = new_api.pull_range()
            times.set_config_timestamp()
            
            test_csv_path = 'C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\test_data.csv'
            test_pickle_path = 'C:\\Users\\jfellow\\OneDrive - Bastian Solutions\\TestCode\\Python\\crossChex_App\\csv\\test_data.pkl'
            
            # Structure is header and payload. Payload is what we need.
            
            
            with open(test_csv_path, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in raw_list:
                    
                    writer.writerow(row)
            print(f"CSV file saved to {test_csv_path}")
            
            with open(test_pickle_path, 'wb') as file:
                pickle.dump(raw_list, file)
    
            
            print(f"raw list: {raw_list}")
            print("Pause for debug")
            
            # Test for now. Need to insert creating a filename.
            # with open(test_csv_path)
            
            
# Time to logic this. We're only going ot pull an API if it's for today,
# AND the previous month of days is not present.
# How in-depth do we want to go with the folder structure? It will all be dynamic, but still...
            
            if emergency:
                #TODO: Pull today's list onsite
                
                # Check for minute or less since last request.
                must_countdown = times.minute_less()
                # If must_countdown = (True, seconds), start countdown
                if must_countdown[0]:
                    print("60 seconds hasn't elapsed since the last API request")
                    print("60 seconds MUST elapse between requests")
                    times.countdown(must_countdown[1])
                    # ^^ ends with 'moving on' messgae.
                
                # If not emergency.. get the report type and adjust dates accordingly.
                
                
                
                
                # wrap in a try to make sure the config time gets reset.
                try:
                    # Instance of API
                    new_api = API()

                    # Pull today's (based on default)
                    new_list = new_api.pull_today()
                    
                    print(new_list)
                    # Cool. now we have the list for a day.
                    # Pass it through and create a function for who's onsite.
                    # Now sort, and evaluate the data.
                    onsite_list = util.who_onsite(new_list, site)
                    print(f"List of onsite personnel = {onsite_list}")


                    # for now, exit the program.
                    raise SystemExit
                        # Filter list by devices
                        # Export a list of poeple (all badge-ins)
                        # export the list of who's clocked in.
                        # Exit program.
                except Exception as e:
                    logging.error(f"Unable to get initial API instance {e}")
                    times.set_config_timestamp()
                    logging.info("At least the config_timestamp was reset")
                    raise SystemExit

                    
                    
                #TODO: Exit the program.
                # Else:
                    # Check for historical data to work with.
                    # Only pull an API if it's incomplete.
                    # Complete the historical 
                    # Set up the request
                        # Considerations:
                            # Hours
                            # groups
                            # site(s)
            # More items to add/consider/rules:
                # When was the last request pulled?
                # Is it end of day request? Clock out all that's still clocked in.
                    # Not considered a pull for the day.
                # Historical day will be checked and filled in the next day
                    # Folder structure for the historical - that's findable by date
                    # How far to check back? 1 week? it shouldn't be more than a day or two.
                # Could DSR have two components
                    # Count of people clocked in from each group, then total manhours for previous day?

            if not emergency:
                
                # Which report is the user wanting?
                report_message = util.report_message(site_config)
                data_type = util.get_num_selection(report_message, 1, len(site_config['Report']), 'because')
                logging.info(f"User selected data type: {data_type}")

                # Respond to the report request. ie, get all remaining info.
                # EOD:
                
                # Month : Need to pull data? or hours? or both?
                
                # Date Range:
                
                try:
                    # Instance of API
                    new_api = API()

                    # Based on data_type TODO: What info changes on API?
                    # for pickle, let's just pull a week's worth to work with.
                    new_api.begin_time = api.begin_of_day(datetime.now() - timedelta(days=7))
                    new_api.end_time = api.end_of_day(datetime.now())

                    
                    # Pull today's (based on default)
                    new_list = new_api.pull_today()
                    
                    
                            
                    # Cool. now we have the list for a day.
                    # Pass it through and create a function for who's onsite.
                    # Now sort, and evaluate the data.
                    onsite_list = util.who_onsite(new_list, site)
                    print(f"List of onsite personnel = {onsite_list}")


                    # for now, exit the program.
                    raise SystemExit
                        # Filter list by devices
                        # Export a list of poeple (all badge-ins)
                        # export the list of who's clocked in.
                        # Exit program.
                except Exception as e:
                    logging.error(f"Unable to get initial API instance {e}")
                    times.set_config_timestamp()
                    logging.info("At least the config_timestamp was reset")
                    raise SystemExit
                

            # Is a data pull necessary?
            # TODO: some check for the last pulled data. If not emergency, or EOD then we look at this.
            #  If EOD, then 
            # New instance of API class. Will naturally get its own token.
            new_api = API()
            
            print(f"number of pages necessary: {new_api.page_num}")     

                    
            to_exit = input(messages.loop_program_message)
            
            if to_exit.lower() == 'exit':
                exit
            
    except Exception as e:
        logging.critical(f"Program closed when it wasn't supposed to. Error: {e}")
        print(f"critical error: Program closed when it wasn't supposed to. Error: {e}")
        
        ### Use an input to manually close the program after failure.
        input("Press Enter to Exit... (disgracefully)")
    
    except KeyboardInterrupt:
        logging.info("G'day, mate.")
        print("g'day, mate")
    
    except SystemExit:
        logging.info("Program exited safely on its own")
    else:
        logging.info("Successful completion of the program. Goodbye")
        


if __name__ == "__main__":
    main()
else:
    print("program has exited")
    logging.info("Program has exited\n\n\n^^^^^^^^\n\n\n")