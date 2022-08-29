

menuText = """
Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
"""

def startupText(inputObj):
    return f"""
Holiday Management
===================
There are {inputObj.numHolidays()} holidays stored in the system.
"""

addHolidayText = """
Add a Holiday
=============
Holiday: """
