Web Sheets
==========

A web-based python spreadsheet app.

Each book has multiple sheets a pre and post script.
Each sheet has a 2D array of cells.
Each cell contains a string of python code which is evaluated
and the result is displayed.
The pre script runs before cells are evaluated and the globals
dictionary from the script is used in evaluating the cells.
The post-script runs after cell evaluation and has access to
cell values.

Documentation_

.. _Documentation: http://web-sheets.readthedocs.io/en/dev

Installation
------------

To install from source::

    sudo -H ./install.bash

This will install the python modules from source, copy files into /lib/systemd/system, and
create folders in /etc/ and /var/log/.

Also need to build handsontable::

    cd handsontable
    npm install
    grunt --force
    

Philosophy
----------

For now, the goal is to keep the sheets module as small as possible.
So features that would require additional code but could be implemented
by the user will not be added.
I will, however, provide as many examples of ideas for user-implemented features as possible.

Modules
=======

sheets
------

Contains the data and methods for spreadsheets.
The basic structure is shown in the following pseudocode.::

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

- Reset globals
  - Construct a new globals dict which contains
    - \_\_builtins\_\_: a dict which contains approved python builtin functions
      and custom implementations of certain other python builtin function
    - sheets: a dict with pairs of sheet keys and numpy arrays. the arrays contain
      the cell strings.
- Execute script\_pre
  - script\_pre is passed the globals object from above
- Evaluate cells
  - For cell evaluation, a shallow copy is made of the globals object from above.
    Therefore, the cell can alter non-trivial objects in the globals.

## sheets\_backend


## web\_sheets\_django

The website itself is powered by Django.
The sheet app handles the viewing and modification of spreadsheets.

# Accessing Sheet Data

    sheet = sheets_backend.sockets.SheetProxy(sheet_id, port)
    sheet.set_cell(0, 0, 'hello')
    ret = sheet.get_sheet_data()

This code will only work if there is a sockets server running at the port specified and a sheet with id sheet\_id exists.

# Production Server

 * change folder and file permission to allow database write
 * set WSGI python path for my custom modules
 * remove references to my environment variables

Development
===========

Install all module from source with::

  pip3 install .

Using the ``-e`` option does not work because it 
does not properly handle subdirectory modules.

Process Layout
==============

We will think about layout in terms of processes.
Processes can be on the same machine or on opposite sides
of the Earth, it makes no difference here.
A plus sign will indicate one or more processes.

Simplest
--------

The simplest setup has a single server 
with storage included.::

    django+
     |
     V
    Server(Storage)

Router
------

A server router can route connections from django
processes to one of multiple server processes.::

    django+
     |
     V
    ServerRouter(Storage) --> Server+

Storage Server
--------------

We can take multiple instances of the simplest
setup and move storage to a single storage server.::

    ___________
    (         )
    ( django+ )
    (  |      )
    (  V      )
    ( Server  )
    (_________)+
       |
       V
    StorageServer

Migration
=========

We need to make sure that when new versions are released, existing
books still load properly from storage.

We will create a test case which will load all books from storage and
possible test some of their functionality.

Testing
=======

For tests requiring a running sheets_backend Server, a server will be started
using a port that is designated for testing.





