## Main app run.
from api_pull import API
from export_csv import CSV_EXPORT
from datetime import date, datetime, timedelta
import messages
from exception import NotInRange
from report import report
import scratch
import csv
import os
import math
import signal
import time
import logging
from logging.handlers import RotatingFileHandler

# Configure the basic logging.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Set up logging.
handler = RotatingFileHandler('crossChexLog.log', maxBytes=10*1024*1024, backupCount=5) #Rotate every 10 Mb, and keep up to 5.
handler.setLevel(logging.INFO)

# Configure logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(handler)

logging.info('Starting Application') # This one isn't running.
logging.warning('example of a warning message')
logging.error('This is what an error looks like!')


# Running logic
running = True

def signal_handler(sig, frame):
    global running
    print("Signal received, exiting gracefully...")
    logging.info('Selected to close via ctrl + c')
    running = False

# Set up the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Ensure the CSV directory exists.
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    try:
        # Make sure the directory for the csv files exists.
        csv_directory = "csv"
        ensure_directory_exists(csv_directory) # def located above.

        while running:


            # get the report info started.
            first_report = report() #Report class
            # Report will automatically run the necessary inputs.
            
            # Instance of API
            first_token = API()
                        
            # Set to the report settings.
            first_token.set_begin_time(first_report.startDate)
            first_token.set_end_time(first_report.endDate)
            
            # first_report.site won't be used until we're sifting through data already pulled.
            # Run a report now?
            logging.info('Pulling the first API request')
            csv_list = first_token.get_full_list_by_start_stop(first_token.begin_time, first_token.end_time)
            # (CSV_LIST [LName, FName, Workno, DeviceName, date of punch, time of punch])
        

            # Create the CSV_EXPORT object and print to file. Data, semi-raw.
            csv_export = CSV_EXPORT(csv_list, first_report.purpose)
            csv_export.print_to_file()

            # Now further working with the list:
            # Sort list from the csv_list (parameters from the user input)
            # Sorted by index 2 (workno).
            sorted_list = sorted(csv_list, key=lambda x: x[2])


            idList = []
            # first_report.site is the site number

            # TODO: Move this to a function in scratch?
            for list in sorted_list:
                
                # If All was selected, then the device name is irrelevant. (site = 1)
                if first_report.site == 1:
                    # No filter. Get for all.
                    idList.append([(str(list[1]) + " " + str(list[0])),list[2], list[3], list[4], list[5]])

                # Else if... the device matches one of the devices for a site, based on site selected.
                # ie. if TJX Marshalls or Office (both should match the same .site), then yes.
                elif list[3] in scratch.site_num_to_device(first_report.site):
                    # Filter by site.
                    idList.append([(str(list[1]) + " " + str(list[0])),list[2], list[3], list[4], list[5]])
                    
            

                    
            # Should be ready to run with any of the site selections.
            inOutList = scratch.assign_in_out(idList)


            # Run who's on site using the inOut list and site num.
            try:
                onsiteToday = scratch.who_on_site_today(inOutList, first_report.site)
            except Exception as e:
                print(f"who_on_site_today: {e}")
                input("Press enter to exit...") # This will keept he console open until pressing enter.
            else:
                input("press enter to exit...")

            counter = 1
            print("Onsite today at " + scratch.site_num_to_name(first_report.site))
            for item in onsiteToday:
                print(str(counter) + ". " + str(item))
                counter += 1

            # first_list = firstToken.get_full_list_by_start_stop(firstToken.begin_time,firstToken.end_time)
            # test_export = CSV_EXPORT("first_file.csv")
            # print("fileName = " + str(test_export.fileName))
            # test_export.change_name_to_timestamp(datetime.now())

            # type_of_report = get_report_length(messages.report_length) <-- returns int to work with.
            ## what are the variables we need to run different reports?
            ### when(date), how much (length of report), where (site)(site isn't relevant with the pull request)

            
            # # Export as a CSV. Create the csv and print it out.
            # csv_export = CSV_EXPORT(csv_list, "past_fortnight")
            # csv_export.print_to_file()
    except Exception as e:
        print(f"an error occurred and now we know where to start: {e}")
        input("Press enter to exit...") # This will keept he console open until pressing enter.
    else:
        input("Press Enter to exit... (Successfully!)")




if __name__ == "__main__":
    main()
    print("Program has exited.")

    '''
    Wisdom: We can only get in touch with our own source of intuition and wisdom,
    when we no longer depend upon others' opinions for our sense of identity or worth.
    '''