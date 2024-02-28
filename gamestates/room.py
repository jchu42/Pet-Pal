from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet

class Room(GameState):
    # def mainPetOnInit(self): #making it readable for you is not good, but you have to make it readable for other people - separate this shit into separate classes
    #     self.imgVel = (0, 0)
    #     self.imgPos = (30, 30)
    #     self.hiddenPos = (30, 30)
    #     return True
    # def mainPetOnTick(self, prevPos):
    #     self.accel = ((random.random() - 0.5)*(0.5 - abs(self.hiddenPos[0]/60 - 0.5)) - ((self.hiddenPos[0]/60 - 0.5)**3)*random.random() ,
    #             (random.random() - 0.5)*(0.5 - abs(self.hiddenPos[1]/60 - 0.5)) - ((self.hiddenPos[1]/60 - 0.5)**3)*random.random() )
    #     self.imgVel = (self.imgVel[0]*0.9 + self.accel[0], self.imgVel[1]*0.9 + self.accel[1])
    #     self.hiddenPos = (self.hiddenPos[0] + self.imgVel[0], self.hiddenPos[1] + self.imgVel[1])
    #     if (self.willChangeFrame()):
    #         return self.setPos (self.hiddenPos)
    # def mainPetOnClick (self, pos):
    #     print ("AA")


    


    def getName(self):
        return "room"

    def loadState(self, *args, **wargs)->None:
        # self.gm.assignMesh(mainPet, "test")
        # self.gm.assignInit(mainPet, self.mainPetOnInit)
        # self.gm.assignTick(mainPet, self.mainPetOnTick)
        # self.gm.assignMouseUp(mainPet, self.mainPetOnClick)
        # self.gm.assignDelete(mainPet, lambda self:print("*dies*"))

        self.mainUI("room2")

        mainPet = MainPet (self.gm)
        
        textTest = GameObject (self.gm).setPos((30, 70)).setImageText("fdsfa", (255, 0, 0, 255), True)
        #self.gm.assignText (textTest, "agfdgdfsfds", (255, 0, 0, 255), True)
        # self.gm.assignInit (textTest, lambda self: self.setPos((30, 70)))
        self.gm.assignMouseUp(textTest, lambda go, pos: self.setState("room2"))

