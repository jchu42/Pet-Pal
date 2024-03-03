from gameobject import GameObject
import random
import gamemanager
from typing import Self
from imagesdict import ImagesDict
import pygame

class Selector(GameObject):
    # ["room", "room2", "kitchen"]
    def __init__(self, gm:gamemanager, options:list[str], color:tuple[int, int, int, int]=(0, 0, 0, 255))->None:
        GameObject.__init__(self, gm)

        self.options = options
        self.color = color

        self.selection = 0

        self.lessthan = GameObject(gm).setImageText("<", self.color)#GameObject(gm).setImageName(lessthanname)
        self.lessthan.assignMouseUp(self.decrement).assignButton("left", self.decrement)
        self.morethan = GameObject(gm).setImageText(">", self.color)#GameObject(gm).setImageName(morethanname)
        self.morethan.assignMouseUp(self.increment).assignButton("right", self.increment)

        self.setPos((30, 30))
    def setPos(self, pos:tuple[int, int])->Self:
        self._nextPos = pos
        self.setLessThanPos((pos[0] - 20, pos[1]))
        self.setMoreThanPos((pos[0] + 20, pos[1]))
        return self
    
    def setLessThanPos (self, pos:tuple[int, int])->Self:
        self.lessthan.setPos (pos)
        return self
    def setMoreThanPos (self, pos:tuple[int, int])->Self:
        self.morethan.setPos (pos)
        return self
    def getOption (self)->str:
        return self.options[self.selection]

    def increment(self)->None:
        self.playSound(2000)
        self.selection += 1
        if (self.selection >= len(self.options)):
            self.selection = 0
    def decrement(self)->None:
        self.playSound(1000)
        self.selection -= 1
        if (self.selection < 0):
            self.selection = len(self.options) - 1

    def tick(self)->None:
        if (self.getOption() in ImagesDict.images):
            self.setImageName(self.getOption())
        else:
            self.setImageText(str(self.getOption()), self.color)