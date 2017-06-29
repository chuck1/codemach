
CodeMach
========
.. image:: https://travis-ci.org/chuck1/codemach.svg?branch=dev
    :target: https://travis-ci.org/chuck1/codemach
.. image:: https://codecov.io/gh/chuck1/codemach/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chuck1/codemach
.. image:: https://img.shields.io/pypi/v/codemach.svg
    :target: https://pypi.python.org/pypi/codemach

Small module that executes python code objects.

codemach.readthedocs.io

Install
-------

::

    pip3 install codemach

Test
----

::

    git clone git@github.com:chuck1/codemach
    cd codemach
    pipenv install
    pytest

Example
-------

::

    from codemach import Machine

    m = Machine()
    m.verbose = 1

    s = """def func(a, b):\n  return a + b\nfunc(2, 3)"""

    c = compile(s, '<string>', 'exec')

    m.exec(c)

prints the following. Each line shows the opname and the stack after the operation.
::

    ------------- begin exec
              LOAD_CONST [<code object func at 0x7f549d91c930, file "<string>", line 1>]
              LOAD_CONST [<code object func at 0x7f549d91c930, file "<string>", line 1>, 'func']
           MAKE_FUNCTION [<code object func at 0x7f549d91c930, file "<string>", line 1>]
              STORE_NAME []
               LOAD_NAME [<code object func at 0x7f549d91c930, file "<string>", line 1>]
              LOAD_CONST [<code object func at 0x7f549d91c930, file "<string>", line 1>, 2]
              LOAD_CONST [<code object func at 0x7f549d91c930, file "<string>", line 1>, 2, 3]
    ------------- begin exec
               LOAD_FAST [2]
               LOAD_FAST [2, 3]
              BINARY_ADD [5]
            RETURN_VALUE []
    ------------- return
           CALL_FUNCTION [5]
                 POP_TOP []
              LOAD_CONST [None]
            RETURN_VALUE []
    ------------- return

