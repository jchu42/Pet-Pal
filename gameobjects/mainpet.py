from gameobject import GameObject
import random
import gamemanager

class MainPet(GameObject):
    def __init__ (self, gm:gamemanager)->None:
        GameObject.__init__(self, gm, [0.5, 1])

        self.imgVel = (0, 0)
        self.imgPos = (30, 30)
        self.hiddenPos = (30, 30)
        gm.assignMouseDown(self, lambda go, pos:print("AA"))
        self.setImageName("pandaidle")

    def tick(self)->None:
        self.accel = ((random.random() - 0.5)*(0.5 - abs(self.hiddenPos[0]/60 - 0.5)) - ((self.hiddenPos[0]/60 - 0.5)**3)*random.random() ,
                (random.random() - 0.5)*(0.5 - abs(self.hiddenPos[1]/60 - 0.5)) - ((self.hiddenPos[1]/60 - 0.5)**3)*random.random() )
        self.imgVel = (self.imgVel[0]*0.9 + self.accel[0], self.imgVel[1]*0.9 + self.accel[1])
        self.hiddenPos = (self.hiddenPos[0] + self.imgVel[0], self.hiddenPos[1] + self.imgVel[1])

        self.setPos (self.hiddenPos)

        if (self.imgVel [0] < 0): # going left
            self.mirror()
        if (self.imgVel [1] < 0): # going up
            self.setImageName("pandajump")
        else:
            self.setImageName("pandaidle")
