import datetime
from datetime import datetime, date
from distutils.command.config import config
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from config import readJsonLoc
from config import saveJsonLoc



# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

@dataclass
class Holiday:
    name: str
    date: str
      
    
    def __str__ (self):
        return '%s %s' % (self.name, self.date)
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
       self.innerHolidays = []

    def __str__(self):
        return str(self.innerHolidays)
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Object by checking the type
        type(holidayObj)
        if type(holidayObj) != Holiday:
            print("That is not a valid holiday.")
            return
        # Use innerHolidays.append(holidayObj) to add holiday
        self.innerHolidays.append(Holiday(holidayObj.name, holidayObj.date))
        # print to the user that you added a holiday
        print(f"Success! {holidayObj} has been added to the calendar!")


    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for i in self.innerHolidays:
            if i.name == HolidayName and i.date == Date:
                print(f"Success! {i} has been found!")
                # Return Holiday
                return Holiday
            else:
                print("Sorry, that holiday does not exist.")

    def removeHoliday(self, HolidayName):
        # Find Holiday in innerHolidays by searching the name and date combination.
        for i in self.innerHolidays:
            if i.name == HolidayName:
                # remove the Holiday from innerHolidays
                self.innerHolidays.remove(i)
                # inform user you deleted the holiday
                print(f"Success! {i} has been removed!")
                return
            else:
                print("Sorry, that holiday does not exist.")

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, "r") as f:
            data = json.load(f)
            for i in data['holidays']:
                self.addHoliday(Holiday(i["name"], i["date"]))
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation,"w") as holidayJSON:
            tempHolidayList = []
            for i in self.innerHolidays:
                holiday = {"name":i.name, "date":i.date}
                tempHolidayList.append(holiday)
            json.dump(tempHolidayList,holidayJSON, indent = 4)
            holidayJSON.write("\n")

        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future.
        try:
            holidays = []
    
            for year in range(2020,2025):
                html = requests.get(f'https://www.timeanddate.com/holidays/us/{year}?hol=33554809')

                soup = BeautifulSoup(html.text, 'html.parser')
                table = soup.find('table', attrs={'id':'holidays-table'})
                body = table.find('tbody')

                for row in body.find_all('tr'):
            
                    #Holiday Dictionary
                    holidayDict = {}

                    date = row.find('th')
                    name = row.find('a')

                #check rows where date and name are not None
                    if date is not None and name is not None:
                
                        date = date.text
                        date = f"{date} {year}"
                        date= datetime.strptime(date,"%b %d %Y")
                        date = date.strftime('%Y-%m-%d')
                
                        holidayDict['Name'] = name.text
                        holidayDict['Date'] = date
            
                    holidays.append(holidayDict)

                    #remove empty dictionaries from list
                    while {} in holidays:
                        holidays.remove({}) 

                    #removing duplicate holidays
                    holidays = [dict(t) for t in {tuple(d.items()) for d in holidays}]

            for i in holidays:
                hol = (Holiday(i['Name'], i['Date']))
                if hol not in self.innerHolidays:
                    self.innerHolidays.append(hol)
        
        except Exception as e:
            print(e)   

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return (len(self.innerHolidays))
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Cast filter results as list
        holidays = list(filter(lambda x: datetime.strptime(x.date, '%Y-%m-%d').isocalendar()[0] == int(year) and datetime.strptime(x.date, '%Y-%m-%d').isocalendar()[1] == int(week_number), self.innerHolidays))
        # return your holidays
        return holidays
        # Week number is part of the the Datetime object

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        for i in holidayList:
            print(str(i))
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        currentWeek = datetime.today().isocalendar().week
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(self.filter_holidays_by_week(datetime.today().year, currentWeek))
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results


def main():
    global readJsonLoc
    global saveJsonLoc
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    initList = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    initList.read_json(readJsonLoc)
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    initList.scrapeHolidays()
    # 3. Create while loop for user to keep adding or working with the Calender
    menuUP = True
    savedWork = False

    print("Holiday Management")
    print("===================")
    print(f"There are {initList.numHolidays()} holidays stored in the system.")
    #print(initList)
    
    while menuUP:
    # Display User Menu (Print the menu)
        print("Holiday Menu")
        print("===================")
        print("1. Add a Holiday")
        print("2. Remove a holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        menuChoice = int(input("Please type the menu option number you'd like to go to: "))
        if menuChoice == 1:
            print("Add a Holiday")
            print("===================")
            holidayChoice = str(input("Holiday: "))
            dateChoice = input("Date (YYYY-MM-DD): ")
            initList.addHoliday(Holiday(holidayChoice, dateChoice))
        elif menuChoice == 2:
            print("Remove a Holiday")
            print("===================")
            holidayNameChoice = str(input("Holiday Name: "))
            initList.removeHoliday(holidayNameChoice)
        elif menuChoice == 3:
            print("Saving Holiday List")
            print("===================")
            wantSave = str(input("Save your changes? [Y/N]: "))
            if wantSave == "Y":
                initList.save_to_json(saveJsonLoc)
                print("Success! Your changes have been saved!")
                savedWork = True
            else:
                print("Changes were not saved.")
        elif menuChoice == 4:
            print("View Holidays")
            print("===================")
            yearChoice = input("Which year?: ")
            weekChoice = input("Which week? [1-52, leave blank for current week]: ")
            if weekChoice == "":
                initList.viewCurrentWeek()
            else:
                print(f"These are the holidays for {yearChoice} week {weekChoice}:")
                initList.displayHolidaysInWeek(initList.filter_holidays_by_week(yearChoice, weekChoice))
        elif menuChoice == 5:
            if savedWork == True:
                exitChoice = input("Are you sure you want to exit? [Y/N]: ")
                if exitChoice == 'Y':
                    print('Goodbye!')
                    break
                elif exitChoice == 'N':
                    continue
            elif savedWork == False:
                unsavedExitChoice = input("Are you sure you want to exit? Your changes will be lost! [Y/N]: ")
                if unsavedExitChoice == 'Y':
                    print("Goodbye!")
                    break
                elif unsavedExitChoice == 'N':
                    continue





           




    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





