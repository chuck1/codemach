import numpy


class CellHelper(object):
    """
    An instance of this class is added to the globals of the ``eval`` call for each cell.
    This class provides access to information about a cell.
    """
    def __init__(self, r, c):
        """
        :param int r: row index
        :param int c: column index
        """
        self.r = r
        self.c = c

class SheetHelper(object):
    """
    we must be careful not to expose too much to the user
    such that he or she may break the program or cause security issues

    .. WARNING::
       passing the sheet to this object is not OK for final implementation
    """
    def __init__(self, sheet_id=None):
        """
        :param sheet_id: index of sheet to be referenced or None to reference current sheet
        """

        self.__book = _global__book

        if sheet_id is None:
            self.__sheet = _global__sheet
        else:
            self.__sheet = self.__book.sheets[sheet_id]
    
    def __getitem__(self, args):
        """
        :param r: row index
         :type r: integer or slice
        :param c: column index
        :type c: integer or slice or None
        :return: array of cell values
        :rtype: `numpy array`_

        .. _numpy array: https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html
        """

        return self.__sheet.array_values(*args)

class BookHelper(object):
    def __init__(self):
        self.__book = __book


