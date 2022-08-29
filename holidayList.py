"""
HolidayList class designed to do most of the data structure storage;
We will also store our Holiday dataclass here.  The class is too small to move
to another file.

class HolidayList:
     - stores holiday objects
     - can add, find, delete holiday from structure
     - readsjson and adds holiday from json
     - saves holidays to a json.
     - scrapeHolidays -> method for grabbing holiday details off the internet
     - numHolidays returns the length of the inner list.
     ToDo:
     - filterHolidaysByWeek
     - displayHolidaysInWeek
     - getWeather
     - viewCurrentWeek

Json structure:
 -  dictionary with one key storing a list of dictionaries.
 - ["holidays"][0]["name" or "date"]
 - So, each holiday must store the name: str and date: datetime
"""

import json
import datetime
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

@dataclass
class Holiday:
    name: str
    date: datetime.date
    
    def __str__ (self):
        return f"{self.name} occurs on {self.date}"

class HolidayList:

    def __init__(self):
        self.holidayObjStorage = []

    def addHoliday(self, holidayObj):
        #check for the type of the holiday object.
        if type(holidayObj) != Holiday:
            return False
        if self.findHoliday(holidayObj.name, holidayObj.date)[1] == False:
            self.holidayObjStorage.append(holidayObj)
        print("You've successfully added a holiday.")

    """
    Searches through the list, if the name and the date are the same, return holiday object and True, otherwise, return None and False.
    """
    def findHoliday(self, holidayName, holidayDate):
        for holiday in self.holidayObjStorage:
            if holidayName == holiday.name and holidayDate == holiday.date:
                return holiday, True
        return None, False

    def findHolidayGeneric(self, holidayInput):
        if type(holidayInput) == datetime:
            for holiday in self.holidayObjStorage:
                if holidayInput == holiday.date:
                    return holiday, True
            return None, False
        elif type(holidayInput) == str:
            for holiday in self.holidayObjStorage:
                if holidayInput == holiday.name:
                    return holiday, True
            return None, False
        else:
            print("You've inputted a value that is not valid, please input a valid option.")
            return None, False


    def removeHoliday(self, holidayName, holidayDate):
        for holiday in self.holidayObjStorage:
            if holidayName == holiday.name and holidayDate == holiday.date:
                self.holidayObjStorage.pop(holiday)
        return False

    def removeHolidayGeneric(self, holidayInput):
        removedObj = False
        if type(holidayInput) == datetime:
            for holiday in self.holidayObjStorage:
                if holidayInput == holiday.date:
                    self.holidayObjStorage.pop(holiday)
                    removedObj = True
            return removedObj
        elif type(holidayInput) == str:
            for holiday in self.holidayObjStorage:
                if holidayInput == holiday.name:
                    self.holidayObjStorage.pop(holiday)
                    removedObj = True
            return removedObj
        else:
            print("You've inputted a value that is not valid, please input a valid option.")
            return removedObj

    def readJson(self, fileLocation):
        with open(fileLocation, "r") as jsonFile:
            data = json.load(jsonFile)
        jsonKeys = list(data.keys())
        for dataDay in data[jsonKeys[0]]:
            self.addHoliday(Holiday(dataDay['name'], datetime.date.fromisoformat(dataDay['date'])))

    def numHolidays(self):
        return len(self.holidayObjStorage)
