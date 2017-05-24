
import contextlib

class Context(object):
    NONE = 0
    SCRIPT = 1
    CELL = 2

@contextlib.contextmanager
def script_exec(book, script):
    old, book.context = book.context, Context.SCRIPT
    yield
    book.context = old

