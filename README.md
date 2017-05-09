# Web Sheets

A web-based python spreadsheet app.

Each sheet has an array of cells and a script.
Each cell contains a string of python code which is evaluated and the result is displayed.
The script runs before cells are evaluated and the globals dictionary from the script is used in evaluating the cells.

## Philosophy

For now, the goal is to keep the sheets module as small as possible.
So features that would require additional code but could be implemented by the user will not be added.

# Components
## Website

The website itself is powered by Django.
The sheet app handles the viewing and modification of spreadsheets.

## sheets Module

The data and methods for the spreads themselves.

## sheets\_backend Module

This module defines an abstract class SheetProxy that
defines all the methods of Sheet that a client needs.
Derived versions of this class can use different backends for
storage and access of actual Sheet objects.

# Accessing Sheet Data

    sheet = SheetProxy(sheet_id, port)
    sheet.set_cell(0, 0, 'hello')
    ret = sheet.get_sheet_data()


