

class Storage(object):
    """
    An abstaction for reading and writing sheets to
    and from long term storage
    """
    def get_object(self, object_id):
        pass

    def save_object(self, object_id):
        pass

class StorageProxy(object):
    """
    This class is an abstraction for access to a
    Book object through communication with a Server
    object.
    """
    pass



