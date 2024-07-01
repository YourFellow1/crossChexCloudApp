# API request with the API class.
import util
from logger_config import logger as logging
from datetime import date, datetime, date, time, timedelta
from requests import request
import json
from math import ceil


config_data = util.read_config()
api_config = config_data['API']


# Set the timestamp to morning (just after midnight)
def begin_of_day(timestamp):
    return timestamp.replace(hour=0, minute=0, second=0)

# Set the timestamp to evening (just after midnight.)
def end_of_day(timestamp):
    return timestamp.replace(hour=23, minute=59, second=59)



class API:
    
    
    
    
    def __init__(self):
        config_data = util.read_config()
        api_config = config_data['API']
        print(f"api_config: {api_config}")
        # Get the config data into the class (init)
        self.headerId = api_config['headerid']
        self.api_key = api_config['api_key']
        self.api_secret = api_config['api_secret']
        self.url = api_config['url']
        
        # Other info at startup.
        self.timestamp = datetime.now()
        
        # Beginning and ending time (Default to today access)
        self.begin_time = begin_of_day(self.timestamp)
        self.end_time = end_of_day(self.timestamp)
        
        # -------- MISC -------------
        # Page_num to iterate multi-pages
        self.page_num = 1
        
        # num_per_page to start with 1.
        self.num_per_page = 1
        
        # Default workno = ''
        self.workno = ''
        
        # Token is mandatory for a pull, so it's part of init.
        self.token = self.get_token()
    
    # Returns the token for the main API request.    
    def get_token(self):
        # Send a request and get the authorize.token for full requests.
        payload={'header[nameSpace]': 'authorize.token',
                    'header[nameAction]': 'token',
                    'header[requestId]': str(self.headerId),
                    'header[timestamp]': str(self.timestamp),
                    'payload[api_key]': str(self.api_key),
                    'payload[api_secret]': str(self.api_secret)
                    }
        
        # Response - Json - pull the token only.
        response = request("POST", self.url, data=payload)
        response_json = json.loads(response.text)
        return response_json['payload']['token']
    
    
    
    # Single request? to set up for a full request?
    def get_single_request(self):
        
        # single record payload.
        payload={'header[nameSpace]': 'attendance.record',
                 'header[nameAction]': 'getrecord',
                 'header[version]': '1.0',
                 'header[requestId]': str(self.headerId),
                 'header[timestamp]': str(self.begin_time),
                 'authorize[type]': 'token',
                 'authorize[token]': str(self.token),
                 'payload[being_time]': str(self.begin_time),
                 'payload[end_time]': str(self.end_time),
                 'payload[workno]': str(self.workno),
                 'payload[order]': 'asc',
                 'payload[page]': str(self.page_num),
                 'payload[per_page]': str(self.num_per_page)}

        # Get the response. Then Json.loads the text of the response.
        response = request("POST", self.url, data=payload)
        return json.loads(response.text)
    
    # Full list of data. We'll work with it after we get the data.
    # What's our default amount of info that we're pulling?
    # Whatever we pull, we need to be ready to make it work with our info.
    
    def pull_last_month(self, begin, end):
        # get the num of pages necessary.
        pass
    
    
    # Get data for onsite's today.
    def pull_today(self):
        # Create list for info we're grabbing. 
        today_list = []

        # Change the 'self' to 100 records per page.
        self.num_per_page = 100
        
        # Leave in the default dates of today.
        
        # get the num of pages necessary.
        loops = self.set_page_num()
        
        # Loop through and pull the data.
        while self.page_num <= loops:
            
            # Run request, change pageNum for next loop, and append to list.
            today_list.append(self.get_single_request())
            self.page_num += 1
            
        return today_list

            
        
    
    
    # Get num of pages needed for the total request.
    def set_page_num(self):
        try:
            # Pull a single request with the given dates, and get num_of_pages.
            # Will produce a num of records, right? Do we leave it at 1 per page?
            response_text = self.get_single_request()
            records = response_text['payload']['pageCount']
            
            # take records. divide by 10 and do ceiling. that will be num of pages for request.
            return ceil(records/100)
        except Exception as e:
            logging.error("Set_Page_num failed for : {e}")
            
    def clear_to_default(self):
        #TODO: put all the values back to default (before program loops around? is this necessary?)
        pass
