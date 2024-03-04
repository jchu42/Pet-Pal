from gameobject import GameObject
import random
import gamemanager
from typing import Self
from imagesdict import ImagesDict
import pygame

class Selector(GameObject):
    # ["room", "room2", "kitchen"]
    def __init__(self,  options:list[str], color:tuple[int, int, int, int]=(0, 0, 0, 255))->None:
        GameObject.__init__(self)

        self.options = options
        self.color = color

        self.selection = 0

        self.lessthan = self.add_child_object(GameObject()).set_image_text("<", self.color)#GameObject(gm).setImageName(lessthanname)
        self.lessthan.on_mouse_up.append(self.decrement)
        self.lessthan.on_button.append(("left", self.decrement))
        self.morethan = self.add_child_object(GameObject()).set_image_text(">", self.color)#GameObject(gm).setImageName(morethanname)
        self.morethan.on_mouse_up.append(self.increment)
        self.morethan.on_button.append(("right", self.increment))

        self.set_pos((30, 30))
    def set_pos(self, pos:tuple[int, int])->Self:
        self._next_pos = pos
        self.lessthan.set_pos((pos[0] - 20, pos[1]))
        self.morethan.set_pos((pos[0] + 20, pos[1]))
        return self
    
    # def set_lessthan_pos (self, pos:tuple[int, int])->Self:
    #     self.lessthan.set_pos (pos)
    #     return self
    # def set_morethan_pos (self, pos:tuple[int, int])->Self:
    #     self.morethan.set_pos (pos)
    #     return self
    def get_option (self)->str:
        return self.options[self.selection]

    def increment(self)->None:
        self.play_sound(2000)
        self.selection += 1
        if (self.selection >= len(self.options)):
            self.selection = 0
    def decrement(self)->None:
        self.play_sound(1000)
        self.selection -= 1
        if (self.selection < 0):
            self.selection = len(self.options) - 1

    def tick(self)->None:
        if (self.get_option() in ImagesDict.images):
            self.set_image_name(self.get_option())
        else:
            self.set_image_text(str(self.get_option()), self.color)