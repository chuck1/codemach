
import json
import logging
import logging.config

class Cell(object):
    def __init__(self, string, value):
        self.string = string
        self.value = value

class Server(object):
    """
    This class is an abstaction for sending and
    receiving book data to and from a BookProxy object.
    The purpose of the Server is to keep
    Book objects loaded in memory.
    """
    def __init__(self, storage):
        """
        :param storage: a Storage object
        """
        self.storage = storage

    def get_book(self, book_id):
        return self.storage.get_object(book_id)

    def save_book(self, book_id):
        return self.storage.save_object(book_id)

class BookProxy(object):
    """
    This class is an abstraction for indirect access to a Book object.
    Implementations shall define all the methods of Book that a client needs.
    """
    pass


