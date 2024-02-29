from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Room(GameState):
    def getName(self)->str:
        return "room"

    def loadState(self, *args, **wargs)->None:
        self.mainUI("room2")

        mainPet = MainPet (self.gm, "panda").setPos((30, 30))
        
        textTest = GameObject (self.gm).setPos((30, 69)).setImageText("frefGvVB", (255, 0, 0, 255), True).assignMouseUp(lambda pos: self.setState("texttest"))

        censoredTest = StrInput (self.gm).setPos ((10, 10)).setColor((0, 255, 255, 0)).setCensored(True)