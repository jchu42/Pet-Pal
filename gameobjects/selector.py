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
    def __init__(self,  options:list[str], initial_selection:int=0,
                 color:tuple[int, int, int, int]=(0, 0, 0, 255))->None:
        GameObject.__init__(self)

        self._options = options
        self._color = color

        self.__selection = initial_selection

        self.lessthan = self.add_child_object(GameObject()).set_image_text("<", self._color)
        self.lessthan.set_origin((0.5, 0.5))
        self.lessthan.on_mouse_up.append(self.__decrement)
        self.lessthan.on_button.append(("left", self.__decrement))
        self.morethan = self.add_child_object(GameObject()).set_image_text(">", self._color)
        self.morethan.set_origin((0.5, 0.5))
        self.morethan.on_mouse_up.append(self.__increment)
        self.morethan.on_button.append(("right", self.__increment))

        self.set_pos((30, 30))
        self.set_origin((0.5, 0.5))

    def set_pos(self, pos:tuple[int, int])->Self:
        self._next_pos = pos
        self.lessthan.set_pos((pos[0] - 20, pos[1]))
        self.morethan.set_pos((pos[0] + 20, pos[1]))
        return self

    def get_option (self)->str:
        """Get the currently selected option.

        Return:
            str
                The currently selected option
        """
        return self._options[self.__selection]

    def __increment(self)->None:
        self.play_sound(71)
        self.__selection += 1
        if self.__selection >= len(self._options):
            self.__selection = 0
    def __decrement(self)->None:
        self.play_sound(59)
        self.__selection -= 1
        if self.__selection < 0:
            self.__selection = len(self._options) - 1

    def tick(self)->None:
        if self.get_option() in ImagesDict.images:
            self.set_image_name(self.get_option())
        else:
            self.set_image_text(str(self.get_option()), self._color)
