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

from logger_config import logger as logging



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


def main():
    global mainLoopCounter
    global emergency
    global site_config
    # Overall try/catch
    try:
        # Make sure the directory for the CSV files exists.
        csv_directory = 'historical csv files'
        util.ensure_directory_exists(csv_directory)
        
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
            site = util.get_num_selection(site_message, 1, len(site_config['Sites']), 'because')
            logging.info(f"selected site: {site}")
            
            # Check for an emergency situation.
            emergency = util.get_emergency()
                        
            if emergency:
                #TODO: Pull today's list onsite
                    # Run API pull to get token
                    # Run API pull w/token.
                    # Make list a dictionary.
                    # Filter list by devices
                    # Export a list of poeple (all badge-ins)
                    # export the list of who's clocked in.
                pass
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
                            
                    
            
            
    except Exception as e:
        logging.critical(f"Program closed when it wasn't supposed to. Error: {e}")
        print(f"critical error: Program closed when it wasn't supposed to. Error: {e}")
        
        ### Use an input to manually close the program after failure.
        input("Press Enter to Exit... (disgracefully)")
        
    else:
        logging.info("Successful completion of the program. Looping back around")
        
        ### Use an input ot manually close go back to the front of the loop.
        input(messages.loop_program_message)


if __name__ == "__main__":
    main()
else:
    print("program has exited")
    logging.info("Program has exited\n\n\n^^^^^^^^\n\n\n")