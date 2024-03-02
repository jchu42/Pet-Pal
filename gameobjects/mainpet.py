from gameobject import GameObject
from gameobjects.status import Status
from typing import Self
from imagesdict import ImagesDict
import random
import gamemanager

class MainPet(GameObject):
    def __init__ (self, gm:gamemanager, petType:str)->None:
        # pet selection?
        # idle, happyidle (default to idle if happyidle does not exist), 
        # movehori, movevert (default to movehori if does not exist)
        # eat (default to movevert, and then to movehori if does not exist)
        # dead (ends at last frame and then stays still) (decrement self.__frame in tick to stay at last/second-last frame)

        GameObject.__init__(self, gm, [0.5, 1])

        gm.assignMouseDown(self, lambda:print("AA"))
        self.petType = petType
        self.setImageName(self.petType + "idle")

        self.__happy = 59
        self.happy = 5

        Status(gm, self)

        self.right = True
        self.action = "idle"
        self.actionValue = 0
        self.changeAction = True

    def setImageName(self, name:str|list[str])->Self:
        if (type(name) == str):
            if (not self.petType in name):
                name = self.petType + name
        else:
            for oneName in name:
                if ((self.petType + oneName) in ImagesDict.images):
                    name = self.petType + oneName
                    break
        if (name != self._imageName):
            self._imageName = name
            self._frame = 0 # reset animation state on name change
        return self
    
    def tick(self)->None:
        self.__happy -= 1
        if (self.__happy < 0):
            self.__happy = 59
        self.happy = int(self.__happy / 10)

        # idle, idle2, idle3...
        # move, movevert (defaults to move > idle)
        # sleep (defaults to idle)
        # eat (defaults to movevert > move > idle)
        # die (defaults to idle)
        # poop (defaults to move)
        if self.changeAction:
            self.changeAction = False
            decision = random.random() * 5
            if (decision > self.happy):
                decision = random.random() * 5
                if (decision > self.happy):
                    self.action = "sleep"
                    self.actionValue = int(random.random()*30) + 30
                else:
                    self.action = "idle"
                    self.actionValue = int(random.random()*15)
            else:
                if (random.random() > 0.5):
                    self.action = "move"
                    self.actionValue = int(random.random()*40) + 10
                else:
                    self.action = "movevert"
                    self.actionValue = int(random.random()*25) + 30
        
        if (self.action == "sleep"):
            self.setImageName(["sleep", "idle"])
            self.actionValue -= 1
            if (self.actionValue <= 0):
                self.changeAction = True
        elif (self.action == "idle"):
            self.setImageName("idle")
            self.actionValue -= 1
            if (self.actionValue <= 0):
                self.changeAction = True
        elif (self.action == "move"):
            self.setImageName(["move", "idle"])
            if (self.getPos()[0] < self.actionValue):
                self.right = True
                self.setPos ((self.getPos()[0] + 1, self.getPos()[1]))
            elif (self.getPos()[0] > self.actionValue): 
                self.right = False
                self.setPos ((self.getPos()[0] - 1, self.getPos()[1]))
            elif (self.getPos()[0] == self.actionValue):
                self.changeAction = True
        elif (self.action == "movevert"):
            self.setImageName(["movevert", "move", "idle"])
            if (self.getPos()[1] < self.actionValue):
                self.setPos ((self.getPos()[0], self.getPos()[1] + 1))
            elif (self.getPos()[1] > self.actionValue):
                self.setPos ((self.getPos()[0], self.getPos()[1] - 1))
            elif (self.getPos()[1] == self.actionValue):
                self.changeAction = True

        if (not self.right):
            self.mirror()
