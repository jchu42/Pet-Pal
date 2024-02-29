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

        self.setPos((30, 30))

        self.options = options

        #self.assignKeyPress(self.handleKeyPress)

        lessthanname = "fontlessthan" + ' '.join(map(str, color)) 
        if (lessthanname not in ImagesDict.images):
            lessthan = ImagesDict.images["fontlessthan"][0].copy()
            lessthan.fill(color, special_flags=pygame.BLEND_MAX)
            ImagesDict.images [lessthanname] = {} 
            ImagesDict.images [lessthanname][0] = lessthan
        morethanname = "fontmorethan" + ' '.join(map(str, color)) 
        if ("fontmorethan" + ' '.join(map(str, color)) not in ImagesDict.images):
            morethan = ImagesDict.images["fontmorethan"][0].copy()
            morethan.fill(color, special_flags=pygame.BLEND_MAX)
            ImagesDict.images [morethanname] = {} 
            ImagesDict.images [morethanname][0] = morethan
        
        self.selection = 0

        self.lessthan = GameObject(gm).setImageName(lessthanname).setPos((10, 30))
        self.lessthan.assignMouseUp(self.decrement).assignButton("left", self.decrement)
        self.morethan = GameObject(gm).setImageName(morethanname).setPos((50, 30)).assignMouseUp(self.increment)
        self.morethan.assignMouseUp(self.increment).assignButton("right", self.increment)
    def setLessThanPos (self, pos:tuple[int, int])->Self:
        self.lessthan.setPos (pos)
        return self
    def setMoreThanPos (self, pos:tuple[int, int])->Self:
        self.morethan.setPos (pos)
        return self
    def getOption (self)->str:
        return self.options[self.selection]

    def increment(self)->None:
        self.selection += 1
        if (self.selection >= len(self.options)):
            self.selection = 0
    def decrement(self)->None:
        self.selection -= 1
        if (self.selection < 0):
            self.selection = len(self.options) - 1

    def tick(self)->None:
        self.setImageName(self.getOption())

    def getText (self)->str:
        return self.text
    #def handleKeyPress (self, key:str):
    #    pass
