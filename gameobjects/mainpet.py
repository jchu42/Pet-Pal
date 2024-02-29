from gameobject import GameObject
from gameobjects.status import Status
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

        # self.imgVel = (0, 0)
        # self.imgPos = (30, 30)
        # self.hiddenPos = (30, 30)
        gm.assignMouseDown(self, lambda go, pos:print("AA"))
        self.petType = petType
        self.setImageName(self.petType + "idle")

        self.__happy = 59
        self.happy = 5

        Status(gm, self)

        self.right = True
        self.action = "idle"
        self.actionValue = 0
        self.changeAction = True

    def tick(self)->None:
        self.__happy -= 1
        if (self.__happy < 0):
            self.__happy = 59
        self.happy = int(self.__happy / 10)

        # self.accel = ((random.random() - 0.5)*(0.5 - abs(self.hiddenPos[0]/60 - 0.5)) - ((self.hiddenPos[0]/60 - 0.5)**3)*random.random() ,
        #         (random.random() - 0.5)*(0.5 - abs(self.hiddenPos[1]/60 - 0.5)) - ((self.hiddenPos[1]/60 - 0.5)**3)*random.random() )
        # self.imgVel = (self.imgVel[0]*0.9 + self.accel[0], self.imgVel[1]*0.9 + self.accel[1])
        # self.hiddenPos = (self.hiddenPos[0] + self.imgVel[0], self.hiddenPos[1] + self.imgVel[1])

        # self.setPos (self.hiddenPos)

        # if (self.imgVel [0] < 0): # going left
        #     self.mirror()
        # if (self.imgVel [1] < 0): # going up
        #     self.setImageName("pandajump")
        # else:
        #     self.setImageName("pandaidle")

        if self.changeAction:
            self.changeAction = False
            decision = random.random() * 5
            if (decision > self.happy):
                self.action = "idle"
                self.actionValue = int(random.random()*10)
            else:
                if (random.random() > 0.5):
                    self.action = "jumphori"
                    self.actionValue = int(random.random()*40) + 10
                else:
                    self.action = "jumpvert"
                    self.actionValue = int(random.random()*25) + 30
        
        if (self.action == "idle"):
            self.setImageName(self.petType + "idle")
            self.actionValue -= 1
            if (self.actionValue <= 0):
                self.changeAction = True
        elif (self.action == "jumphori"):
            self.setImageName(self.petType + "jump")
            if (self.getPos()[0] < self.actionValue):
                self.right = True
                self.setPos ((self.getPos()[0] + 1, self.getPos()[1]))
            elif (self.getPos()[0] > self.actionValue):
                # going to left
                self.right = False
                self.setPos ((self.getPos()[0] - 1, self.getPos()[1]))
            elif (self.getPos()[0] == self.actionValue):
                self.changeAction = True
        elif (self.action == "jumpvert"):
            self.setImageName(self.petType + "jump")
            if (self.getPos()[1] < self.actionValue):
                self.setPos ((self.getPos()[0], self.getPos()[1] + 1))
            elif (self.getPos()[1] > self.actionValue):
                self.setPos ((self.getPos()[0], self.getPos()[1] - 1))
            elif (self.getPos()[1] == self.actionValue):
                self.changeAction = True
        if (not self.right):
            self.mirror()

        if (self.action == "idle"):
            self.actionValue -= 1
