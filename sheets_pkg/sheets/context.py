
import contextlib

class Context(object):
    NONE = 0
    SCRIPT = 1
    CELL = 2

@contextlib.contextmanager
def context(book, context):
    old = book.context
    book.context = context
    try:
        yield
    finally:
        book.context = old

