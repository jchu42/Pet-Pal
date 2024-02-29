from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector

class RoomSelector(GameState):
    def getName(self)->str:
        return "roomselector"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((0, 0, 0, 255))

        selector = Selector(self.gm, ["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        selector.setLessThanPos((5, 65)).setMoreThanPos((55, 65))

        nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        nextButton.assignMouseUp(lambda: self.setState("room", roomname=selector.getOption()))
        nextButton.assignButton("return", lambda:self.setState("password", username=self.username.getText()))
        #GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 69)).assignMouseUp(lambda go, pos: self.setState("room"))

    # def nextButtonAction (self, key:str):
    #     if (key == "return"): # enter button pressed
    #         self.setState("password", username=self.username.getText())