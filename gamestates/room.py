from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Room(GameState):
    def getName(self)->str:
        return "room"

    def loadState(self, roomname:str, petname:str, *args, **wargs)->None:
        self.mainUI(roomname)

        mainPet = MainPet (self.gm, petname).setPos((30, 30))
        
        textTest = GameObject (self.gm).setPos((30, 69)).setImageText("frefGvVB", (255, 0, 0, 255), True).assignMouseUp(lambda: self.setState("texttest"))
