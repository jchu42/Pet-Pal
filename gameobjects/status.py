"""This module contains the Status GameObject for use with MainPet.

This module isn't really needed - could just be a regular GameObject that shows the staus in MainPet
"""
from typing import Self
from gameobject import GameObject

class Status(GameObject):
    """Show the MainPet's status icon.
    
    ...
    
    Attributes
    ----------
    happiness : int
        The happiness value to show
    """
    def __init__ (self)->None:
        """Initialize the Status GameObject"""
        GameObject.__init__(self)
        self.happiness = 0
        self.set_origin ((0.5, 1))
    def set_happiness (self, value:int)->Self:
        """Set the happiness value image

        Parameters
        ----------
        value : int
            The happiness value (0-5)
        
        Returns
        -------
        GameObject
            self
        """
        self.happiness = value
        return self
    def tick(self)->None:
        self.set_image_name("happy" + str(self.happiness))
