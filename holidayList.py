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
     - filterHolidaysByWeek
     - displayHolidaysInWeek
     - getWeather
     - viewCurrentWeek

Json structure:
 -  dictionary with one key storing a list of dictionaries.
 - ["holidays"][0]["name" or "date"]
 - So, each holiday must store the name: str and date: datetime
"""

from calendar import week
import json
import datetime
import time
from bs4 import BeautifulSoup
import requests 
from dataclasses import dataclass
from config import *

'''
using @dataclass decorator for convenience
'''
@dataclass
class Holiday:
    name: str
    date: datetime.date
    
    def __str__ (self):
        return f"{self.name} ({self.date})"

'''
Main datastructure, arguably some of the functions in main.py could be moved here.
'''
class HolidayList:

    def __init__(self):
        self.holidayObjStorage = []

    def toDict(self):
        dictionaryStorage = {"holidays": []}
        for obj in self.holidayObjStorage:
            dictionaryStorage["holidays"].append({"name": obj.name, "date": str(obj.date)})
        return dictionaryStorage

    '''
    notably has a backup findHoliday check, there are several generic versions of functions for potential future code
    expansion
    '''
    def addHoliday(self, holidayObj):
        #check for the type of the holiday object.
        if type(holidayObj) != Holiday:
            return False
        if self.findHoliday(holidayObj.name, holidayObj.date)[1] == False:
            self.holidayObjStorage.append(holidayObj)

    """
    Searches through the list, if the name and the date are the same, return holiday object and True, otherwise, 
    return None and False.
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
        for index, holiday in enumerate(self.holidayObjStorage, start=0):
            if holidayName == holiday.name and holidayDate == holiday.date:
                self.holidayObjStorage.pop(index)
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

    '''
    Initial setup methods and helper functions.
    '''
    def readJson(self, fileLocation):
        with open(fileLocation, "r") as jsonFile:
            data = json.load(jsonFile)
        jsonKeys = list(data.keys())
        for dataDay in data[jsonKeys[0]]:
            self.addHoliday(Holiday(dataDay['name'], datetime.date.fromisoformat(dataDay['date'])))

    def numHolidays(self):
        return len(self.holidayObjStorage)

    def saveToJson(self, fileLocation, jsonReadyDict):
        jsonString = json.dumps(jsonReadyDict, indent = 4)
        with open(fileLocation, 'w') as jsonFile:
            jsonFile.write(jsonString)

    def monthToDigit(self, month):
        monthToValue = [("Jan", 1), ("Feb", 2), ("Mar", 3), ("Apr", 4), ("May", 5), ("Jun", 6),
        ("Jul", 7), ("Aug", 8), ("Sep", 9), ("Oct", 10), ("Nov", 11), ("Dec", 12)]
        for index in range(len(monthToValue)):
            if month == monthToValue[index][0]:
                return monthToValue[index][1]

    def scrapeForDates(self):
        currentYear = datetime.date.today().isocalendar()[0]
        minYear = currentYear - 2
        maxYear = currentYear + 3 #because of the exclusivity on range()
        for year in range(minYear, maxYear):
            response = requests.get(url + f"{year}")
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', attrs = {"id":"holidays-table"})
            tbody = table.find('tbody')
            
            holidayNames = []
            holidayDates = []
            #print(tbody.find_all('th')[0].string.split(" "))
            for date in tbody.find_all('th'):
                hDate = date.string.split(" ")
                hDate[0] = self.monthToDigit(hDate[0])
                hDate = datetime.date(int(year), hDate[0], int(hDate[1]))
                holidayDates.append(hDate)

            for holiday in tbody.find_all('a'):
                hName = holiday.string
                holidayNames.append(hName)

            for iter in range(len(holidayNames)):
                if not self.findHoliday(holidayNames[iter], holidayDates[iter])[1]:
                    self.addHoliday(Holiday(holidayNames[iter], holidayDates[iter]))


    def filterHolidaysByWeek(self, year, weekNumber):
         holidays = list(filter(lambda holidayListed: holidayListed.date.isocalendar()[0] == year and holidayListed.date.isocalendar()[1] == weekNumber,
         self.holidayObjStorage))
         return holidays

    def displayHolidaysInWeek(self, year, weekNumber):
        holidaysInWeek = self.filterHolidaysByWeek(year, weekNumber)
        print(f"\n\nThese are the holidays for {year} week #{weekNumber}:")
        for holi in holidaysInWeek:
            print(str(holi))

    '''
    Almost identical to display Holidays in week but now we make an api call.
    Theoretically that api call works, but my api key seems to not be activated yet.
    '''
    def getWeather(self, weekNumber, yearInput):
        if int(yearInput) > datetime.date.today().isocalendar()[0]:
            print("Sorry, we can't predict the future. There will be no weather output.")
            return
        datesThatMatter = self.filterHolidaysByWeek(int(yearInput), int(weekNumber))
        weatherJsonList = []
        for index in range(len(datesThatMatter)):
            response = requests.get(apiUrl2.format(apiKey2, datesThatMatter[index].date))
            weatherJsonList.append(response.json()['forecast']['forecastday'][0]['day']['condition']['text'])

        print(f"\n\nThese are the holidays for {yearInput} week #{weekNumber}:")
        for index, holi in enumerate(datesThatMatter, start=0):
            print(f"{str(holi)} - {weatherJsonList[index]}")
