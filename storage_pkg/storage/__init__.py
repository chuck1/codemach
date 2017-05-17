

class Storage(object):
    """
    An abstaction for reading and writing sheets from
    and to long term storage.
    """
    def get_object(self, object_id):
        pass

    def save_object(self, object_id):
        pass

class StorageProxy(object):
    """
    This class is an abstraction for indirect access to a Storage object.
    """
    pass



