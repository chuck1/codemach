
class NotAllowedError(Exception):
    """
    Raised during script exec or cell eval when a potential
    security risk is detected.
    """
    def __init__(self, message):
        super(NotAllowedError, self).__init__(message)

