
CodeMach
========

Tiny module that executes python code objects.

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

       LOAD_CONST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>]
       LOAD_CONST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 'func']
    MAKE_FUNCTION [<code object func at 0x7f38c20df9c0, file "<string>", line 1>]
       STORE_NAME []
        LOAD_NAME [<code object func at 0x7f38c20df9c0, file "<string>", line 1>]
       LOAD_CONST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2]
       LOAD_CONST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2, 3]
        LOAD_FAST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2, 3, 2]
        LOAD_FAST [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2, 3, 2, 3]
       BINARY_ADD [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2, 3, 5]
     RETURN_VALUE [<code object func at 0x7f38c20df9c0, file "<string>", line 1>, 2, 3]
    CALL_FUNCTION [5]
          POP_TOP []
       LOAD_CONST [None]
     RETURN_VALUE []

