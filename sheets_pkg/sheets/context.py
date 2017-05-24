
import contextlib

class Context(object):
    NONE = 0
    SCRIPT = 1
    CELL = 2

@contextlib.contextmanager
def script_exec(book, script):
    assert(book.context == 0)
    old = book.context
    book.context = Context.SCRIPT
    yield
    book.context = old

@contextlib.contextmanager
def cell_eval(book, sheet, cell):
    assert(book.context == 0)
    old = book.context
    book.context = Context.CELL
    yield
    book.context = old

@contextlib.contextmanager
def context(book, context):
    assert(book.context == 0)
    old = book.context
    book.context = context
    yield
    book.context = old

