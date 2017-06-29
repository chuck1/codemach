
.. testcode::

    from codemach import Machine

    m = Machine(verbose=True)
    
    s = """
    def func(a, b):
        return a + b
    func(2, 3)"""

    c = compile(s, '<string>', 'exec')

    m.exec(c)

Below is the output. Each line shows the opname and the stack after the operation.

.. testoutput::

    ------------- begin exec
    LOAD_CONST           ['<code object func at 0x7f3732a3fed0, file "<string>", line 2>']
    LOAD_CONST           ['<code object func at 0x7f3732a3fed0, file "<string>", line 2>', "'func'"]
    MAKE_FUNCTION        ['<FunctionType object, function <function func at 0x7f3732951730>>']
    STORE_NAME           []
    LOAD_NAME            ['<FunctionType object, function <function func at 0x7f3732951730>>']
    LOAD_CONST           ['<FunctionType object, function <function func at 0x7f3732951730>>', '2']
    LOAD_CONST           ['<FunctionType object, function <function func at 0x7f3732951730>>', '2', '3']
    ------------- begin exec
    LOAD_FAST            ['2']
    LOAD_FAST            ['2', '3']
    BINARY_ADD           ['5']
    RETURN_VALUE         []
    ------------- return
    CALL_FUNCTION        ['5']
    POP_TOP              []
    LOAD_CONST           ['None']
    RETURN_VALUE         []

