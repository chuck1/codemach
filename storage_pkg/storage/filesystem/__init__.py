import os
import pickle
import logging

import storage

logger = logging.getLogger(__name__)

class Storage(storage.Storage):
    
    def __init__(self, cls, folder):
        self.cls = cls
        self.folder = folder
        self.objects = {}
        self.__object_new_args = ()
    
    def set_object_new_args(self, args):
        self.__object_new_args = args

    def next_id(self):
        if os.path.exists(os.path.join(self.folder, 'object_id.txt')):
            with open(os.path.join(self.folder, 'object_id.txt'), 'r') as f:
                i = int(f.read())

            i += 1
        else:
            i = 0
        
        try:
            os.makedirs(self.folder)
        except FileExistsError as e: pass

        with open(os.path.join(self.folder, 'object_id.txt'), 'w') as f:
            f.write(str(i))

        return str(i)

    def object_new(self):
        b = self.cls(*self.__object_new_args)
        i = self.next_id()
        self.objects[i] = b
        self.write(i, b)
        return i, b

    def get_object(self, object_id):
        if not object_id in self.objects:
            self.objects[object_id] = self.read(object_id)
        
        return self.objects[object_id]

    def save_object(self, object_id):
        if not object_id in self.objects:
            raise RuntimeError('attempt to save sheet that is not loaded')

        self.write(object_id, self.objects[object_id])

    def read(self, object_id):
        """
        :param object_id: sheet id

        returns sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(object_id)+'.bin')
        
        #if not os.path.exists(filename):

        with open(filename, 'rb') as f:
            o = pickle.loads(f.read())
        
        if not isinstance(o, self.cls):
            raise TypeError()

        return o

    def write(self, object_id, object):
        """
        :param object_id: sheet id
        :param sheet: sheets.Sheet object
        """
        filename = os.path.join(self.folder, str(object_id)+'.bin')
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(object))

