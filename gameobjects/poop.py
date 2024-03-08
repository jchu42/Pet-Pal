"""This module contains poop.py's Poop GameObject"""
import random
from gameobject import GameObject


class Poop(GameObject):
    """Poopy

    ...

    Attributes
    ----------
    
    """
    def __init__ (self, layer:int=1, **wargs)->None:
        """Poop the poop"""
        GameObject.__init__(self, layer=layer, **wargs)

        self.set_image_name("poop")
        self.set_pos((int(random.random()*40 + 12), int(random.random()*40 + 12)))
        self.set_frames_per_frame(3)
        self.on_mouse_up.append(self.poopydi_scoop)

        self.queue_sound([x +20 for x in range(10)][int(random.random()*10)], 
                         [20, 25, 7][int(random.random()*3)], 
                         [x + 100 for x in range(20)][int(random.random()*20)]) # poopy sound

        self._mirrored = random.random()>0.5
        self.__animate_poop_pop = False

    def poopydi_scoop (self)->None:
        """Play poop.py's Poop poop pop part"""
        self.__animate_poop_pop = True
        self.on_mouse_up = []
        self.set_image_name("poopclean")
        self.set_frames_per_frame(1)

    def tick(self)->None:
        if self.__animate_poop_pop:
            if self._frame == self._num_frames() - 1:
                self.set_deleted()
