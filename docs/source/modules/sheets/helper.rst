======
helper
======

An instance of ``CellHelper`` and ``CellsHelper`` are available as globals in the evaluation of each cell.

Classes
=======

.. py:class:: CellHelper

.. py:attribute:: r

   row index

.. py:attribute:: c

   column index

.. py:class:: CellsHelper

.. py:classmethod:: __getitem__(r, c=None, sheet_id=None)

   :param r: row index
   :type r: integer or slice
   :param c: column index
   :type c: integer or slice or None
   :param sheet_id: index of sheet to be referenced or None to reference current sheet
   :return: array of cell values
   :rtype: numpy array



