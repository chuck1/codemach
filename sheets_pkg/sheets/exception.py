

class NotAllowedError(Exception):
    def __init__(self, message):
        super(NotAllowedError, self).__init__(message)

