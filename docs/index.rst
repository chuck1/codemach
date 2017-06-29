.. codemach documentation master file, created by
   sphinx-quickstart on Wed Jun 28 19:38:57 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

codemach
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   module/index.rst
   development.rst

Small module that executes python code objects.

This module was created to solve the security issues
associated with execution of arbitrary code strings.
The Machine class can execute python code objects
and allow the user to intervene.

.. include:: ../README.rst
   :start-line: 13
   :end-line: -1

Operations
----------

140 CALL_FUNCTION_VAR
~~~~~~~~~~~~~~~~~~~~~

need more testing, but in one test, was used to call a function defined as

::

    def foo(*args):
        pass

where TOS1 is the function object and TOS is a tuple of arguments

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


