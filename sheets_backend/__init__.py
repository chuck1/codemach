
class Storage(object):
    """
    An abstaction for reading and writing sheets to
    and from long term storage
    """
    def read(sheet_id): pass
    def write(sheet_id, b):
        """
        :param b: bytes
        """
        pass
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

class SheetProxy(object):
    """
    This class is an abstraction for access to a
    Sheet object through communication with a Server
    object.
    """
    





