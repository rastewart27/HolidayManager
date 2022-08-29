"""
Got annoyed with all the text on the starter code, we're writing this one my way.
"""


'''
Main function for interaction and object creation.
'''
from holidayList import *
from textBlocks import *
import time
import datetime

def addHoliday(holidayListObj):
    print(addHolidayText)
    holidayName = input().strip().lower()
    needProperDate = True
    while needProperDate:
        print("Date: ")
        holidayDate = input().strip().lower()
        try:
            holidayDate = datetime.date.fromisoformat(holidayDate)
        except:
            print("Please input your date in the yyyy-mm-dd format.  Thank you.")
            continue
        needProperDate = False
    holidayListObj.addHoliday(Holiday(holidayName, holidayDate))
    


def main():
    newHolidayList = HolidayList()
    newHolidayList.readJson("holidays.json")
    print(startupText(newHolidayList))
    time.sleep(3)
    stillGoing = True
    while stillGoing:
        print(menuText)
        userMenuSelection = input().strip().lower()[0]
        if userMenuSelection.isnumeric() != True:
            print("Please enter a number for your selection.")
            continue
        userMenuSelection = int(userMenuSelection)
        if userMenuSelection == 1:
            addHoliday(newHolidayList)
        elif userMenuSelection == 2:
            continue
        elif userMenuSelection == 5:
            stillGoing = False




if __name__ == "__main__":
    #I hate passing immediately to main() but I'm not sure if that's a convention or not.
    main()