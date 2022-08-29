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

def numericCheck(inputText):
    if inputText.isnumeric() != True:
            print("Please enter a number for your selection.")
            return True
    return False

def alphaCheck(inputText):
    if inputText.isalpha() != True:
        print("Please enter the proper letter(s).")
        return True
    return False

def addHoliday(holidayListObj):
    print(addHolidayText, end = "")
    holidayName = input().strip()
    needProperDate = True
    while needProperDate:
        print("Date: ", end = "")
        holidayDate = input().strip().lower()
        try:
            holidayDate = datetime.date.fromisoformat(holidayDate)
        except:
            print("Error:\nPlease input your date in the yyyy-mm-dd format.  Thank you.")
            continue
        needProperDate = False
    holidayListObj.addHoliday(Holiday(holidayName, holidayDate))
    print(f"Success:\n{holidayName} ({holidayDate}) has been added to the holiday list.")

def rmHoliday(holidayListObj, savesToMake):
    print(removeHolidayText, end = "")
    needRemoveHoliday = True
    while needRemoveHoliday:
        holidayName = input()
        returnedTuple = holidayListObj.findHolidayGeneric(holidayName)
        if returnedTuple[1] == False:
            print(f"Error:\n{holidayName} not found.  Would you like to try again? (y/n)", end = "")
            cont = input().strip().lower()[0]
            
            if alphaCheck(cont):
                print("Please input a letter, we'll assume you wish to continue removing holidays")
                continue
            
            if cont == 'n':
                return savesToMake
        else:
            holidayListObj.removeHoliday(returnedTuple[0].name, returnedTuple[0].date)
            print(f"Success:\n{holidayName} has been removed from the holiday list.")
            needRemoveHoliday = False
            return True

def saveHolidayList(holidayListObj, jsonReadyDict):
    userTryingToSave = True
    while userTryingToSave:
        print(saveHolidayText, end = "")
        userIsCrazy = input().strip().lower()[0]
        if alphaCheck(userIsCrazy):
            print("Please input a holiday that has only letters in its name.")
            continue

        if userIsCrazy == 'y':
            holidayListObj.saveToJson("holidaysTested.json", jsonReadyDict) #fix file name  ################################################################################################
            print(successSave)
            userTryingToSave = False
        elif userIsCrazy == 'n':
            print(canceledSave)
            userTryingToSave = False
        else:
            print("Please input the correct character, \'y\' or \'n\'")

def viewHolidayList(holidayListObj):
    print(viewFiles, end = "")
    viewingHolidayList = True
    while viewingHolidayList:
        yearInput = input().strip().lower()
        if numericCheck(yearInput) or len(yearInput) != 4:
            print("A year has to only contain numbers and must be 4 integers long.")
            continue
        viewingHolidayList = False

    while not viewingHolidayList:
        print("Which week? #[1-52, Leave blank for the current week]: ", end="")
        weekInput = input().strip().lower()
        if (numericCheck(weekInput) or len(weekInput) >= 3) and weekInput != "":
            print("Please follow instructions and input the week as a number.")
            continue
        viewingHolidayList = True
        
    if weekInput == "":
        weekInput = datetime.date.today().isocalendar()[1]

    holidayListObj.displayHolidaysInWeek(int(yearInput), int(weekInput))


def exitMenu(savesToMake):
    print(exitMenuText)
    if savesToMake:
        print("Your changes will be lost.")
    print("[y/n] ", end= "")
    cantInputWell = True
    while cantInputWell:
        userDecision = input().strip().lower()[0]

        if not alphaCheck(userDecision):
            cantInputWell = False
    
    if userDecision == 'y':
        print("Goodbye!")
        return True
    else:
        return False
    



def main():
    newHolidayList = HolidayList()
    newHolidayList.readJson("holidays.json")
    newHolidayList.scrapeForDates()
    print(startupText(newHolidayList))
    time.sleep(2)
    
    stillGoing = True
    savesToMake = False
    while stillGoing:
        print(menuText, end = "")
        userMenuSelection = input().strip().lower()[0]
        if numericCheck(userMenuSelection):
            continue
        userMenuSelection = int(userMenuSelection)
        if userMenuSelection == 1:
            addHoliday(newHolidayList)
            savesToMake = True
        elif userMenuSelection == 2:
            savesToMake = rmHoliday(newHolidayList, savesToMake)
        elif userMenuSelection == 3:
            saveHolidayList(newHolidayList, newHolidayList.toDict())
            #print(newHolidayList.toDict())
            savesToMake = False
        elif userMenuSelection == 4:
            viewHolidayList(newHolidayList)
        elif userMenuSelection == 5:
            if exitMenu(savesToMake):
                stillGoing = False




if __name__ == "__main__":
    #I hate passing immediately to main() but I'm not sure if that's a convention or not.
    main()