from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Username(GameState):
    def getName(self)->str:
        return "username"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((0, 0, 0, 255))

        GameObject (self.gm).setImageText("Enter Username", (255, 0, 0, 255), centered=False).setPos((2, 10))
        self.username = StrInput (self.gm).setPos ((4, 16)).setColor((0, 255, 255, 0))

        nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        nextButton.assignMouseUp(lambda: self.setState("password", username=self.username.getText()))
        #nextButton.assignKeyPress(self.nextButtonAction)
        nextButton.assignButton("return", lambda:self.setState("password", username=self.username.getText()))
        #GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 69)).assignMouseUp(lambda go, pos: self.setState("room"))

    # def nextButtonAction (self, key:str):
    #     if (key == "return"): # enter button pressed
    #         self.setState("password", username=self.username.getText())