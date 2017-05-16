======
cell
======

Classes
=======

.. py:class:: Cell

.. py:attribute:: string

   string containing python code

.. py:classmethod:: comp

   Compile the string.
   
   The code object is inspected for possible security issues.
   If any of the values in co_names starts with ``__``, a error is raised.


