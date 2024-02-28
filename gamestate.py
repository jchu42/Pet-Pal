import gamemanager
from gameobject import GameObject

class GameState:
    def __init__(self, gm:gamemanager)->None:
        self.gm = gm
    def getName(self)->str:
        pass
    def loadState(self, *args, **wargs)->None:
        pass
    def stateTick(self)->None:
        pass

    def setState (self, newState:str, *args, **wargs)->None:
        self.gm.setState(newState, *args, **wargs)

    def mainUI(self, room):
        GameObject(self.gm).setImageName("bgwhite").setPos((0, 0)).setOrigin((0, 0))

        GameObject(self.gm).setImageName(room).setPos((0, 0)).setOrigin((0, 0))

        GameObject(self.gm).setImageName("bgblack").setPos((0, 0)).setOrigin((0, 0))