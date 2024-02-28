from gameobject import GameObject
import random
import gamemanager
#from gameobjects.mainpet import MainPet

class Status(GameObject):
    def __init__ (self, gm:gamemanager, mp:GameObject)->None:
        GameObject.__init__(self, gm)
        self.mp = mp
        self.setOrigin ((0.5, 1))
    def tick(self)->None:
        self.setImageName("happy" + str(self.mp.happy))
        self.setPos((self.mp.getPos()[0], self.mp.getPos()[1] - 15)) # some number