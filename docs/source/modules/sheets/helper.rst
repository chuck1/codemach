======
helper
======

An instance of ``CellHelper`` and ``CellsHelper`` are available as globals in the evaluation of each cell.

Classes
=======

CellHelper
----------

:py:attr: r

row index

**c**

column index

CellsHelper
-----------

**__getitem__** (r, c=None, sheet_id=None)

Returns a numpy array of cell values.
*r* and *c* are integers or slices (any valid argument to a numpy.array __getitem__ method).
If *sheet_id* is None, the current sheet is referenced.



