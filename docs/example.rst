
.. testsetup::

    import sys
    import logging
    import codemach
    logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)])
    

.. testcode::

    import logging
    from codemach import Machine

    m = Machine(logging.INFO)
    
    s = """def func(a, b):\n  return a + b\nfunc(2, 3)"""

    c = compile(s, '<string>', 'exec')

    m.exec(c)

Below is the output. Each line shows the opname and the stack after the operation.

.. testoutput::

    ------------- begin exec
    LOAD_CONST           ['<code object fun']
    LOAD_CONST           ['<code object fun', 'func']
    MAKE_FUNCTION        ['<FunctionType ob']
    STORE_NAME           []
    LOAD_NAME            ['<FunctionType ob']
    LOAD_CONST           ['<FunctionType ob', '2']
    LOAD_CONST           ['<FunctionType ob', '2', '3']
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
    ------------- return
