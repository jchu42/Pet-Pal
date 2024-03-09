"""This module contains all exceptions for this package"""

class CharNotFoundException(Exception):
    """This exception is raised when a font image cannot be found in ImageDict."""
class KeyException (Exception):
    """Raised when a key press isn't recognized in StrInput"""
class PetNotFoundException(Exception):
    """Raised when the pet type isn't found"""
class FieldNotFoundException(Exception):
    """Raised when a db field can't be found"""