from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector

class PetSelector(GameState):
    def getName(self)->str:
        return "petselector"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((255, 255, 255, 255))

        selector = Selector(self.gm, ["pandaidle", "catidle"], color=(0, 0, 0, 255))

        nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        nextButton.assignMouseUp(lambda: self.setState("roomselector", petname=selector.getOption().removesuffix("idle")))
        nextButton.assignButton("return", lambda:self.setState("roomselector", petname=selector.getOption().removesuffix("idle")))
       