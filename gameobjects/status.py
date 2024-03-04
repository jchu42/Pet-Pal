from gameobject import GameObject
import random
import gamemanager
#from gameobjects.mainpet import MainPet

class Status(GameObject):
    def __init__ (self, mp:GameObject)->None:
        GameObject.__init__(self)
        self.mp = mp
        self.set_origin ((0.5, 1))
    def tick(self)->None:
        self.set_image_name("happy" + str(self.mp.happy))
        self.set_pos((self.mp.get_pos()[0], self.mp.get_pos()[1] - 15))