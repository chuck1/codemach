
class Cell(object):
    def __init__(self, string, value):
        self.string = string
        self.value = value

class Storage(object):
    """
    An abstaction for reading and writing sheets to
    and from long term storage
    """
    pass

class Server(object):
    """
    This class is an abstaction for sending and
    receiving sheet data to and from a ServerProxy object.
    The purpose of the Server is to keep
    Sheet objects loaded in memory.
    """
    def __init__(self, storage):
        """
        :param storage: a Storage object
        """
        self.storage = storage

    def get_book(self, book_id):
        return self.storage.get_book(book_id)

    def save_book(self, book_id):
        return self.storage.save_book(book_id)

class BookProxy(object):
    """
    This class is an abstraction for access to a
    Book object through communication with a Server
    object.
    """
    pass



