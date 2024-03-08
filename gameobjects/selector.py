"""This module contains the Selector class which is used to create an option selector UI"""
from typing import Self
from gameobject import GameObject
from imagesdict import ImagesDict

class Selector(GameObject):
    """Easily create an option selector with left and right arrows.

    ...

    Attributes
    ----------
    lessthan : GameObject
        The clickable "<" GameObject that decrements the selection option
    morethan : GameObject
        The clickable ">" GameObject that increments the selection option
    """
    def __init__(self,
                 options:list[str],
                 origin=(0.5, 0.5),
                 initial_selection:int=0,
                 color:tuple[int, int, int, int]=(0, 0, 0, 255),
                 pos_all:tuple[int, int]=(30, 30),
                 **wargs)->None:
        """Initialize the Selector and its arrow button GameObjects
        
        Parameters
        ----------
        options : list[str]
            A list of images (or text, if not found) to use as selection options
        initial_selection : int, default=0
            The initial selection this Selector should show to the user
        color : tuple[int, int, int, int], default=(0, 0, 0, 255)
            The color the left and right arrows should be
        """
        GameObject.__init__(self, **wargs)

        self._options = options
        self._color = color

        self.__selection = initial_selection

        self.lessthan = self.add_child_object(GameObject(imagetext=("<", color),
                                                         on_mouse_up=[self.decrement]))
        self.morethan = self.add_child_object(GameObject(imagetext=(">", color),
                                                         on_mouse_up=[self.increment]))
        self.lessthan.set_origin((0.5, 0.5))
        #self.lessthan.on_mouse_up.append(self.decrement)
        self.lessthan.on_button.append(("left", self.decrement))
        self.morethan.set_origin((0.5, 0.5))
        self.morethan.on_mouse_up.append(self.increment)
        self.morethan.on_button.append(("right", self.increment))

        self.set_pos_all(pos_all)
        self.set_origin(origin)

    def set_pos_all(self, pos:tuple[int, int])->Self:
        """Set the position of this Selector and its arrow button GameObjects

        Parameters
        ----------
        pos : tuple[int, int]
            The position this selector's option shown should be
            The arrow button GameObjects are moved to 20 pixels left and right of this position

        Returns
        -------
        Selector
            self
        """
        self._next_pos = pos
        self.lessthan.set_pos((pos[0] - 20, pos[1]))
        self.morethan.set_pos((pos[0] + 20, pos[1]))
        return self

    def get_option (self)->str:
        """Get the currently selected option.

        Returns
        -------
        str
            The currently selected option
        """
        return self._options[self.__selection]

    def increment(self)->None:
        """Change to the next option"""
        self.queue_sound(71)
        self.__selection += 1
        if self.__selection >= len(self._options):
            self.__selection = 0
    def decrement(self)->None:
        """Change to the previous option"""
        self.queue_sound(59)
        self.__selection -= 1
        if self.__selection < 0:
            self.__selection = len(self._options) - 1

    def tick(self)->None:
        if self.get_option() in ImagesDict.images:
            self.set_image_name(self.get_option())
        else:
            self.set_image_text(str(self.get_option()), self._color)
