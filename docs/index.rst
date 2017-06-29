.. codemach documentation master file, created by
   sphinx-quickstart on Wed Jun 28 19:38:57 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to codemach's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   module/index.rst

CodeMach
========

This module was created to solve the security issues
associated with execution of arbitrary code strings.
The Machine class can execute python code objects
and allow the user to intervene.

Handling class method code
--------------------------

The builtin function __build_class__ requires a function
object containing the source code of the class.
If we simple pass this function, it will not be executed
by the machine, but rather by the default implementation.
The solution is to pass a function wrapper the within the
wrapper allow the Machine to execute the actual function
and return the result.

http://grokbase.com/t/python/python-list/033r5nks47/type-function-does-not-subtype#20030324rcnwbkfedhzbaf3vmiuer3z4xq

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

