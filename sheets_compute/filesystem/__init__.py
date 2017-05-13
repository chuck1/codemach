import os
import pickle

import sheets
import sheets_backend

class Storage(sheets_backend.Storage):
    
    def __init__(self, folder):
        self.folder = folder
        self.books = {}

    def next_id(self):
        if os.path.exists(os.path.join(self.folder, 'book_id.txt')):
            with open(os.path.join(self.folder, 'book_id.txt'), 'r') as f:
                i = int(f.read())
        else:
            i = 0
        
        i += 1

        with open(os.path.join(self.folder, 'book_id.txt'), 'w') as f:
            f.write(str(i))

        return str(i)

    def book_new(self):
        b = sheets.Book()
        i = self.next_id()
        self.books[i] = b
        self.write(i, b)
        return i, b

    def get_book(self, book_id):
        if not book_id in self.books:
            self.books[book_id] = self.read(book_id)
        
        return self.books[book_id]

    def save_book(self, book_id):
        if not book_id in self.books:
            raise RuntimeError('attempt to save sheet that is not loaded')

        self.write(book_id, self.books[book_id])

    def read(self, book_id):
        """
        :param book_id: sheet id

        returns sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(book_id)+'.bin')
        
        #if not os.path.exists(filename):

        with open(filename, 'rb') as f:
            o = pickle.loads(f.read())
        
        if not isinstance(o, sheets.Book):
            raise TypeError()

        return o

    def write(self, book_id, book):
        """
        :param book_id: sheet id
        :param sheet: sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(book_id)+'.bin')
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(book))

