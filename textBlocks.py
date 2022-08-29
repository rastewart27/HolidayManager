

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

removeHolidayText = """
Remove a Holiday
================
Holiday Name: """

saveHolidayText = """
Saving Holiday List
====================
Are you sure you want to save your changes? [y/n]: """

canceledSave = """Canceled:
Holiday list file save canceled.
"""

successSave = """Success:
Your changes have been saved.
"""

viewFiles = """View Holidays
=================
Which year?: """

exitMenuText = """Exit
=====
Are you sure you want to exit?"""