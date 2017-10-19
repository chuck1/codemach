codemach
========
.. image:: https://travis-ci.org/chuck1/codemach.svg?branch=master
    :target: https://travis-ci.org/chuck1/codemach
.. image:: https://codecov.io/gh/chuck1/codemach/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chuck1/codemach
.. image:: https://readthedocs.org/projects/codemach/badge/?version=latest
   :target: http://codemach.readthedocs.io/
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/codemach.svg
   :target: https://pypi.python.org/pypi/codemach
.. image:: https://img.shields.io/pypi/pyversions/codemach.svg
   :target: https://pypi.python.org/pypi/codemach

Small module that executes python code objects.

Install
-------

::

    pip3 install codemach

Development
-----------

::

    git clone git@github.com:chuck1/codemach
    cd codemach
    pipenv --python /usr/bin/python3.6
    pipenv install
    pipenv run pip3 install -e .
    pipenv run pytest

Example
-------

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
    LOAD_CONST           [<class 'code'>]
    LOAD_CONST           [<class 'code'>, "'func'"]
    MAKE_FUNCTION        ['<codemach.FunctionType object, function=func>']
    STORE_NAME           []
    LOAD_NAME            ['<codemach.FunctionType object, function=func>']
    LOAD_CONST           ['<codemach.FunctionType object, function=func>', '2']
    LOAD_CONST           ['<codemach.FunctionType object, function=func>', '2', '3']
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

