import logging
from logging.handlers import RotatingFileHandler
import logging.handlers
import main
import globals


#--------- LOGGER SETUP -------------------------

# Create a logger
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

# create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(globals.logFilePath, maxBytes=10*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

#------------- END LOGGER SETUP. -----------------------
