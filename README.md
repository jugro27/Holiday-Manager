# Holiday Manager

This is a program that auto-loads in 7 holidays from a JSON file and then scrapes the rest of the holidays from 2020-2024 and puts them into a JSON out file. There is a UI that allows the user to either add holidays, remove holidays, save their changes, view holidays present, and exit. 

-------------------------------------------------------------------------------------------------------------------------


The URL used to scrape is https://www.timeanddate.com/holidays/us/2022?hol=33554809 


The config.py file is needed to obtain variables used in JSON save/read functions, or you could just use your own file names.

-------------------------------------------------------------------------------------------------------------------------


**Files in Repo:**

.gitignore: obviously ignore it

Holiday-Psuedocode-Planning.txt: pseudocode used prior to beginning coding to plan out approach

README.md: what you're reading right now

calendarHolidays.json: the JSON out file of 7 starter holidays + all holidays scraped from above URL

holiday_startercode.py: main code to run the program

holidays.json: JSON file with 7 holidays that are read in in holiday_startercode.py

-------------------------------------------------------------------------------------------------------------------------


**TO RUN THE SCRIPT YOU MUST HAVE**
1. holiday_startercode.py
2. holidays.json
3. config.py (contact me for file if needed, optional since only used for file names and not any APIs)
