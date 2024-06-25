## class to store the data needed for each report pull
# This doesn't include the data pull. This is just the information packaged as a "report".

from datetime import date, datetime, time, timedelta
import messages
from exception import NotInRange


# Exports a full datetime object based on an input from computer.
def get_date_input(message):
        while True:
            try:
                # enter a date to be returned
                inputDate = input(message)
                
            except ValueError:
                print("Please input as \'2001-06-24\'")
                continue
            else:
                print("Date entered was: " + str(date))
                year, month, day = map(int, inputDate.split('-'))
                fullDate = datetime(year, month, day, 0, 0, 0)

                return fullDate
            

## Def used to get an input number within a range.
# Loop that can be used for any number input. (Int >0 only)
def get_num_selection(message, botRange, topRange):
    while True:
        try:
            response = int(input(message))
            if response > topRange or response < botRange:
                raise NotInRange
            else:
                return response
        except ValueError:
            print("Must be a number")
        except NotInRange:
            print("Number must be in the range of the prompt")

'''
Properties of "report":
reportLength - number selection from the message.
startDate - datetime for the first day of the pull
endDate - datetime for the last day of the pull
purpose - string put together to represent they type of report being pulled.
    will be the name of the output file. Open to changing this.
site - number of site they are pulling.
'''


class report:

    def __init__(self):

        # Ask for this first. Based on this, we can weed out the others.
        self.reportLength = get_num_selection(messages.report_length, 1, messages.num_of_lengths)

        # if 1, then it's today. don't need to call date input Ugly code. GET IT THOUGH!
        if self.reportLength == 1:
            self.startDate, self.endDate = datetime.now(), datetime.now()
            self.purpose = "Today"
        else: # Need to exclude the date range.
            self.startDate = get_date_input(messages.select_date)

        #2 = Single day, but day selected. (selected above from the 'else')
        if self.reportLength == 2:
            self.startDate, self.endDate = datetime.now(), datetime.now()
            self.purpose = "One_Day " + self.startDate.strftime("%m_%d")
        
        #3 = Two Days: selected day plus 1.
        elif self.reportLength == 3:
            self.endDate = self.startDate + timedelta(days=1)
            self.purpose = "Two_Day " + self.startDate.strftime("%m_%d") + "-" + self.endDate.strftime("%m/%d")
        
        #4 = Past Week (from today). Start -7 through now()
        elif self.reportLength == 4:
            self.endDate = self.startDate
            self.startDate = self.startDate - timedelta(days=7)
            self.purpose = "7 days starting_" + self.startDate.strftime("%m_%d")
        
        #5 = Enter date range.
        elif self.reportLength == 5:
            self.startDate = get_date_input(messages.select_start_date)
            self.endDate = get_date_input(messages.select_end_date)
            self.purpose = "Range " + self.startDate.strftime("%m_%d") + self.endDate.strftime("%m_%d")
        
        #6 = Month range. Starts with beginning of selectd month to the end.
        elif self.reportLength == 6:
            ##TODO: need to create the month version.
            # For now, just use the start and end date.
            pass
        
        #7 = Devices are people too.
        elif self.reportLength == 7:
            #TODO: need to create this report.
            pass
        
        
        # site property (number)
        self.site = get_num_selection(messages.report_site, 1, messages.num_of_sites)

        

