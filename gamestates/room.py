from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet

class Room(GameState):
    def getName(self):
        return "room"

    def loadState(self, *args, **wargs)->None:
        self.mainUI("room2")

        mainPet = MainPet (self.gm, "panda").setPos((30, 30))
        
        textTest = GameObject (self.gm).setPos((30, 70)).setImageText("frefGvVB", (255, 0, 0, 255), True).assignMouseUp(lambda go, pos: self.setState("room2"))

