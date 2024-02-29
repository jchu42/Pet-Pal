import gamemanager
from gameobject import GameObject
from imagesdict import ImagesDict
import pygame

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

    def bgColor(self, color:tuple[int, int, int, int]) -> None:
        name = "bg" + ' '.join(map(str, color))
        #print (name)
        if name not in ImagesDict.images:
            bgSurface = ImagesDict.images["bgwhite"][0].copy()#pygame.Surface(ImagesDict.images["bgwhite"][0].copy().get_size())
            #print (bgSurface.get_size())
            bgSurface.fill(color)#, special_flags=pygame.BLEND_MAX)
            ImagesDict.images[name] = {}
            ImagesDict.images[name][0] = bgSurface
        GameObject(self.gm).setImageName(name).setPos((0, 0)).setOrigin((0, 0))

    def mainUI(self, room:str)->None:
        GameObject(self.gm).setImageName("bgwhite").setPos((0, 0)).setOrigin((0, 0))

        GameObject(self.gm).setImageName(room).setPos((0, 0)).setOrigin((0, 0))

        GameObject(self.gm).setImageName("bgblack").setPos((0, 0)).setOrigin((0, 0))