from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Room2(GameState):
    def getName(self):
        return "room2"
    def loadState(self, *args, **wargs)->None:
        self.mainUI ("kitchen")
        textTest = GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 70)).assignMouseUp(lambda go, pos: self.setState("room"))
        inputTest = StrInput (self.gm).setPos ((10, 10)).setColor((0, 255, 255, 0))