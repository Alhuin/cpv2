class Error(Exception):
    """Base class for other exceptions"""
    pass


class CustomError(Error):
    """Raised when I programmatically raise an error"""
    pass
