from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Password(GameState):
    def getName(self)->str:
        return "password"
    def loadState(self, username:str, *args, **wargs)->None:
        self.bgColor ((0, 0, 0, 255))

        GameObject (self.gm).setImageText("Enter Username", (122, 0, 0, 255), centered=False).setPos((2, 10))
        GameObject (self.gm).setImageText(username, (0, 122, 122, 255), centered=False).setPos((4, 16))

        GameObject (self.gm).setImageText("Enter Password", (255, 0, 0, 255), centered=False).setPos((2, 28))        
        StrInput (self.gm).setPos ((4, 34)).setColor((0, 255, 255, 0)).setCensored(True)

        nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        nextButton.assignMouseUp(lambda: self.setState("petselector"))
        # nextButton.assignKeyPress(self.nextButtonAction)
        nextButton.assignButton("return", lambda:self.setState("petselector")) # or just room

        #GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 69)).assignMouseUp(lambda go, pos: self.setState("room"))
        
    # def nextButtonAction (self, key:str)->None:
    #     print (key)
    #     if (key == "return"): # enter button pressed
    #         self.setState("room")