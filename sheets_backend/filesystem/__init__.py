import os
import pickle

import sheets
import sheets_backend

class Storage(sheets_backend.Storage):
    #folder = '/home/crymal/sheets'
    
    def __init__(self, folder):
        self.folder = folder
        self.sheets = {}

    def get_sheet(self, sheet_id):
        if not sheet_id in self.sheets:
            self.sheets[sheet_id] = self.read(sheet_id)
        
        return self.sheets[sheet_id]

    def save_sheet(self, sheet_id):
        if not sheet_id in self.sheets:
            raise RuntimeError('attempt to save sheet that is not loaded')

        self.write(sheet_id, self.sheets[sheet_id])

    def read(self, sheet_id):
        """
        :param sheet_id: sheet id

        returns sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(sheet_id)+'.bin')
        
        if not os.path.exists(filename):
            o = sheets.Sheet()
            return o

        with open(filename, 'rb') as f:
            o = pickle.loads(f.read())
        
        if not isinstance(o, sheets.Sheet):
            raise TypeError()

        return o

    def write(self, sheet_id, sheet):
        """
        :param sheet_id: sheet id
        :param sheet: sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(sheet_id)+'.bin')
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(sheet))

