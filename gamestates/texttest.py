from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class TextTest(GameState):
    def getName(self)->str:
        return "texttest"
    def loadState(self, *args, **wargs)->None:
        self.mainUI ("kitchen")
        GameObject (self.gm).setImageText("1234567890", (255, 0, 255, 255), True).setPos((30, 6))
        GameObject (self.gm).setImageText("!@#$%^&*()", (255, 0, 255, 255), True).setPos((30, 12))
        GameObject (self.gm).setImageText("-_=+[]{}\\|", (255, 0, 255, 255), True).setPos((30, 18))
        GameObject (self.gm).setImageText(",<.>/?;:'" + '"', (255, 0, 255, 255), True).setPos((30, 24))
        GameObject (self.gm).setImageText("qwertyuiop", (255, 0, 255, 255), True).setPos((30, 30))
        GameObject (self.gm).setImageText("asdfghjk l", (255, 0, 255, 255), True).setPos((30, 36))
        GameObject (self.gm).setImageText("zxcv b n m", (255, 0, 255, 255), True).setPos((30, 42))
        StrInput (self.gm).setPos ((1, 48)).setColor((0, 255, 255, 0))

        GameObject (self.gm).setImageText("go back", (255, 0, 0, 255), True).setPos((30, 69)).assignMouseUp(lambda: self.setState("room"))