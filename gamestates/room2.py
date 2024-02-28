from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet

class Room2(GameState):
    def getName(self):
        return "room2"
    def loadState(self, *args, **wargs)->None:
        self.mainUI ("kitchen")
        textTest = GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 70))
        # self.gm.assignText (textTest, "go back", (255, 0, 0, 255), True)
        #self.gm.assignInit (textTest, lambda self: self.setPos((30, 70)))
        #self.gm.assignMouseUp(textTest, lambda a, pos: self.setState(0))
        self.gm.assignMouseUp(textTest, lambda a, pos: self.setState("room"))