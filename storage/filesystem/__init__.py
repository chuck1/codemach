import os
import pickle

import storage

class Storage(storage.Storage):
    
    def __init__(self, folder):
        self.folder = folder
        self.objects = {}

    def next_id(self):
        if os.path.exists(os.path.join(self.folder, 'object_id.txt')):
            with open(os.path.join(self.folder, 'object_id.txt'), 'r') as f:
                i = int(f.read())
        else:
            i = 0
        
        i += 1

        with open(os.path.join(self.folder, 'object_id.txt'), 'w') as f:
            f.write(str(i))

        return str(i)

    def book_new(self):
        b = sheets.Book()
        i = self.next_id()
        self.objects[i] = b
        self.write(i, b)
        return i, b

    def get_book(self, object_id):
        if not object_id in self.objects:
            self.objects[object_id] = self.read(book_id)
        
        return self.objects[object_id]

    def save_book(self, object_id):
        if not object_id in self.objects:
            raise RuntimeError('attempt to save sheet that is not loaded')

        self.write(object_id, self.objects[book_id])

    def read(self, object_id):
        """
        :param object_id: sheet id

        returns sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(object_id)+'.bin')
        
        #if not os.path.exists(filename):

        with open(filename, 'rb') as f:
            o = pickle.loads(f.read())
        
        if not isinstance(o, sheets.Book):
            raise TypeError()

        return o

    def write(self, object_id, book):
        """
        :param object_id: sheet id
        :param sheet: sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(object_id)+'.bin')
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(book))

