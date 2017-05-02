
class Cell(object):
    def __init__(self, string, value):
        self.string = string
        self.value = value

class Storage(object):
    """
    An abstaction for reading and writing sheets to
    and from long term storage
    """
    def read(self, sheet_id):
        """
        :param sheet_id: sheet id
        """
        raise NotImplementedError()
    def write(self, sheet_id, b):
        """
        :param sheet_id: sheet id
        :param b: bytes
        """
        raise NotImplementedError()

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
        
        self.sheets = {}

    def get_sheet(self, sheet_id):
        if not sheet_id in self.sheets:
            self.sheets[sheet_id] = self.storage.read(sheet_id)
        
        return self.sheets[sheet_id]

class SheetProxy(object):
    """
    This class is an abstraction for access to a
    Sheet object through communication with a Server
    object.
    """
    def set_cell(self, r, c, s):
        """
        proxy of sheets.Sheet.set_cell
        """
        raise NotImplementedError()






