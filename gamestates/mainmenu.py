from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class MainMenu(GameState):
    def getName(self)->str:
        return "mainmenu"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((0, 0, 0, 255))
        
        loginButton = GameObject (self.gm).setImageText("Login", (255, 0, 0, 255), True).setPos((30, 12))
        loginButton.assignMouseUp(lambda: self.setState("username"))
        loginButton.assignButton("return", lambda:self.setState("username"))

        texttestButton = GameObject (self.gm).setImageText("Text Test", (255, 0, 0, 255), True).setPos((30, 24))
        texttestButton.assignMouseUp(lambda: self.setState("texttest"))
        texttestButton.assignButton("return", lambda:self.setState("texttest"))

        audiotestButton = GameObject (self.gm).setImageText("Audio Test", (255, 0, 0, 255), True).setPos((30, 36))
        audiotestButton.assignMouseUp(lambda: self.setState("audiotest"))
        audiotestButton.assignButton("return", lambda:self.setState("audiotest"))

    def changeToPassword (self)->None:
        # todo - combine username and password states; add a back button to go from password back to username
        pass