from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Login(GameState):
    def getName(self)->str:
        return "login"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((0, 0, 0, 255))

        self.enterUser = GameObject (self.gm).setImageText("Enter Username", (255, 0, 0, 255), centered=False).setPos((2, 10))
        self.username = StrInput (self.gm).setPos ((4, 16)).setColor((0, 255, 255, 0))

        self.nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        self.nextButton.assignMouseUp(self.changeToPassword)
        self.nextButton.assignButton("return", self.changeToPassword)

    def changeToPassword (self)->None:
        self.enterUser.setImageText("Enter Username", (122, 0, 0, 255), centered=False)
        GameObject (self.gm).setImageText(self.username.getText(), (0, 122, 122, 255), centered=False).setPos((4, 16))
        self.username.deleteSelf()
        self.nextButton.deleteSelf()

        GameObject (self.gm).setImageText("Enter Password", (255, 0, 0, 255), centered=False).setPos((2, 28))        
        self.password = StrInput (self.gm).setPos ((4, 34)).setColor((0, 255, 255, 0)).setCensored(True).setMuted(True)

        self.nextButton = GameObject (self.gm).setImageText("Next", (255, 0, 0, 255), True).setPos((30, 69))
        self.nextButton.assignMouseUp(lambda: self.setState("petselector"))
        self.nextButton.assignButton("return", lambda:self.setState("petselector"))
