import gamemanager
from imagesdict import ImagesDict
from typing import Self
import pygame

class GameObject:
    def __init__(self, gm:gamemanager, origin:tuple[int, int]=(0.5, 0.5))->None:
        self.gm = gamemanager
        gm.addGameObject(self) # fuggit we ball

        self.__origin = origin

        self.__pos = (0, 0)
        self.__nextPos = (0, 0)
        self.__imageName = ""
        self.__frame = 0

    def tick(self)->None:
        pass

    def draw(self)->None:
        self.__pos = self.__nextPos
        ImagesDict.drawImage(self.__imageName, self.__pos, self.__origin, self.__frame)
        self.__frame += 1
    def setOrigin (self, origin:tuple[int, int])->Self:
        self.__origin = origin
        return self
    def getPos(self)->tuple[int, int]:
        return self.__pos
    def setPos(self, pos:tuple[int, int])->Self:
        self.__nextPos = pos
        return self
    
    def setImageName(self, name:str)->Self:
        if (name != self.__imageName):
            self.__imageName = name
            self.__frame = 0 # reset animation state on name change
        return self

    def __getLengthOfText (self, string:str) -> int:
        startX = -1 # account for space at the end of the text
        for char in string:
            if (char >= 'a' and char <= 'z'):
                img = ImagesDict.images["font" + char + "2"]
            elif (char >= 'A' and char <= 'Z'):
                img = ImagesDict.images["font" + char]
            elif (char == "."):
                img = ImagesDict.images["fontdot"]
            elif (char == "?"):
                img = ImagesDict.images["fontquestion"]
            elif (("font" + char) in ImagesDict.images):
                img = ImagesDict.images["font" + char]
            else:
                print ("Cannot find character: ", char)
            startX += img[0].get_width() + 1 # 1 space in-between characters
        return startX
    
    def setImageText(self, string:str, color=(0, 0, 0, 255), centered = True)->Self:
        name = "TEXT" + ' '.join(map(str, color)) + string + str(centered) # save all copies of colors of strings of text
        if (name) not in ImagesDict.images:
            textSurface = pygame.Surface((self.__getLengthOfText (string), 8), pygame.SRCALPHA) # how tall is the text anyway?
            
            startX = 0 # round up or down? does it matter?

            for char in string:
                if (char >= 'a' and char <= 'z'):
                    img = ImagesDict.images["font" + char + "2"]
                elif (char >= 'A' and char <= 'Z'):
                    img = ImagesDict.images ["font" + char]
                elif (char == "."):
                    img = ImagesDict.images["fontdot"]
                elif (char == "?"):
                    img = ImagesDict.images["fontquestion"]
                elif (("font" + char) in ImagesDict.images):
                    img = ImagesDict.images["font" + char]
                else:
                    print ("char", char, "not found")

                if (color is not (0, 0, 0, 255)):
                    copy = img[0].copy() # required for custom colors....? would it be just faster to do <...>.. yeah, but eh
                    copy.fill(color, special_flags=pygame.BLEND_MAX)
                else:
                    copy = img[0]

                #textSurface.blit (copy, (startX - self.__origin[0] * img[0].get_width(), 0))
                textSurface.blit (copy, (startX, 0))

                startX += img[0].get_width() + 1 # uh huh
            
            ImagesDict.images [name] = {} #ImagesDict.ImageSet(name, self.drawingSurface)
            ImagesDict.images [name][0] = textSurface
            #if (centered):
            #    self.createMesh (name, origin=[0.5,1], framesEachImage = 1)
            #else:
            #    self.createMesh (name, origin=[0,1], framesEachImage = 1)
        if (centered):
            self.__origin = [0.5, 1]
        else:
            self.__origin = [0, 1]
        self.setImageName(name)
        return self
    
    def contains (self, pos:tuple[int, int])->bool:
        frame = self.__frame % len(ImagesDict.images[self.__imageName])
        left = - self.__origin[0] * ImagesDict.images[self.__imageName][frame].get_width() - 1
        top = - self.__origin[1] * ImagesDict.images[self.__imageName][frame].get_height()  - 1 
        right = (1 - self.__origin[0]) * ImagesDict.images[self.__imageName][frame].get_width() 
        bottom = (1 - self.__origin[1]) * ImagesDict.images[self.__imageName][frame].get_height() 
        return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)