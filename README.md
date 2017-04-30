

# Website

The website itself is powered by Django.
The sheet app handles the viewing and modification of spreadsheets.

## accessing sheets

    try:
        sheet = SheetProxy(sheet_id)
    except  as e:
        # handle specific error
    
    sheet.get_all()

    sheet.set((1,1),new_cell_contents)
    
    

# sheets Module

The data and methods for the spreads themselves.
This module is independent of all others

# sheets\_backend Module

This module defines an abstract class SheetProxy that
defines all the methods of Sheet that a client needs.
Derived versions of this class can use different backends for
storage and access of actual Sheet objects.




