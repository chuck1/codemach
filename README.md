# Web Sheets

A web-based python spreadsheet app.

## Website

The website itself is powered by Django.
The sheet app handles the viewing and modification of spreadsheets.

### accessing sheets

    sheet = SheetProxy(sheet_id, port)
    sheet.set_cell(0, 0, 'hello')
    ret = sheet.get_sheet_data()

## sheets Module

The data and methods for the spreads themselves.

## sheets\_backend Module

This module defines an abstract class SheetProxy that
defines all the methods of Sheet that a client needs.
Derived versions of this class can use different backends for
storage and access of actual Sheet objects.




