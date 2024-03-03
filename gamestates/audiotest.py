from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector

class AudioTest(GameState):
    def getName(self)->str:
        return "audiotest"
    def loadState(self, *args, **wargs)->None:
        self.bgColor ((255, 255, 255, 255))

        GameObject(self.gm).setImageText("Pitch").setPos((30, 7))
        self.pitch = Selector(self.gm, [x*25+25 for x in range (160)], color=(255, 0, 0, 255)).setPos((30, 14)).setMuted(True)
        self.pitch.selection = 3
        self.pitch.lessthan.assignMouseUp(self.buttonSound)
        self.pitch.morethan.assignMouseUp(self.buttonSound)
        GameObject(self.gm).setImageText("Instrument").setPos((30, 24))
        self.instrument = Selector(self.gm, [x for x in range (128)], color=(255, 0, 0, 255)).setPos((30, 31)).setMuted(True)
        self.instrument.lessthan.assignMouseUp(self.buttonSound)
        self.instrument.morethan.assignMouseUp(self.buttonSound)
        GameObject(self.gm).setImageText("Volume").setPos((30, 41))
        self.volume = Selector(self.gm, [x*4 for x in range(31)], color=(255, 0, 0, 255)).setPos((30, 47)).setMuted(True)
        self.volume.selection = 25
        self.volume.lessthan.assignMouseUp(self.buttonSound)
        self.volume.morethan.assignMouseUp(self.buttonSound)

        self.playButton = GameObject(self.gm).setPos((30, 58)).setImageText("Play", (255, 0, 255, 255))
        self.playButton.assignMouseDown(self.buttonSound)

        loginButton = GameObject (self.gm).setImageText("Return", (255, 0, 0, 255), True).setPos((30, 69))
        loginButton.assignMouseUp(lambda: self.setState("mainmenu"))
        loginButton.assignButton("return", lambda:self.setState("mainmenu"))

    def buttonSound(self) -> None:
        self.playButton.playSound(self.pitch.getOption(), self.instrument.getOption(), self.volume.getOption())