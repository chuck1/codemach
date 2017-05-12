# Web Sheets

A web-based python spreadsheet app.

Each sheet has an array of cells and a script.
Each cell contains a string of python code which is evaluated and the result is displayed.
The script runs before cells are evaluated and the globals dictionary from the script is used in evaluating the cells.

## Philosophy

For now, the goal is to keep the sheets module as small as possible.
So features that would require additional code but could be implemented by the user will not be added.
I will, however, provide as many examples of ideas for user-implemented features as possible.

# Modules

## sheets

Contains the data and methods for spreadsheets.
The basic structure is shown in the following pseudocode.

    Book:
      sheets = dict of Sheet objects
      script_pre = Script object
      script_post = Script object

    Sheet:
      cells = Cells object
      
    Cells:
      cells = numpy.array of Cell objects

    Cell:
      string = string which gets passed to eval()

    Script:
      string = string which gets passed to exec()

The steps to recalculate the entire book are as follows

- reset globals
  - construct a new globals dict which contains
    - __builtins__: a dict which contains approved python builtin functions
      and custom implementations of certain other python builtin function
    - sheets: a dict with pairs of sheet keys and numpy arrays. the arrays contain
      the cell strings.
      

## sheets\_backend

This module defines an abstract class SheetProxy that
defines all the methods of Sheet that a client needs.
Derived versions of this class can use different backends for
storage and access of actual Sheet objects.

## web\_sheets\_django

The website itself is powered by Django.
The sheet app handles the viewing and modification of spreadsheets.

# Production Server

 * change folder and file permission to allow database write
 * set WSGI python path for my custom modules
 * remove references to my environment variables

# Accessing Sheet Data

    sheet = sheets_backend.sockets.SheetProxy(sheet_id, port)
    sheet.set_cell(0, 0, 'hello')
    ret = sheet.get_sheet_data()

This code will only work if there is a sockets server running at the port specified and a sheet with id sheet_id exists.
