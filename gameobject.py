import gamemanager 
from imagesdict import ImagesDict
from typing import Self
import pygame

class GameObject:
    def __init__(self, gm:gamemanager, origin:tuple[int, int]=(0.5, 0.5))->None:
        self.gm = gm
        gm.addGameObject(self)

        self._origin = origin

        self._pos = None
        self._nextPos = (0, 0)
        self._imageName = ""
        self._framesPerFrame = 1
        self._frame = 0
        self._mirrored = False

    def setFramesPerFrame (self, frames:int)->Self:
        self._framesPerFrame = 1.0/frames
        return self

    def tick(self)->None:
        pass

    def mirror(self)->Self:
        self._mirrored = True
        return self
    def draw(self)->None:
        self._pos = self._nextPos
        ImagesDict.drawImage(self._imageName, self._pos, self._origin, int(self._frame), self._mirrored)
        self._frame += self._framesPerFrame
        self._mirrored = False
    def setOrigin (self, origin:tuple[int, int])->Self:
        self._origin = origin
        return self
    def getPos(self)->tuple[int, int]:
        if (self._pos == None): # if hasn't been initialized yet
            self._pos = self._nextPos
        return self._pos
    def setPos(self, pos:tuple[int, int])->Self:
        self._nextPos = pos
        return self
    
    def setImageName(self, name:str)->Self:
        if (name != self._imageName):
            self._imageName = name
            self._frame = 0 # reset animation state on name change
        return self

    def __getCharImg (self, char:str)-> pygame.Surface:
        if (char >= 'A' and char <= 'Z'):
            char = char.lower()
        if (char >= 'a' and char <= 'z'):
            img = ImagesDict.images["font" + char]
        elif (char == "."):
            img = ImagesDict.images["fontdot"]
        elif (char == "?"):
            img = ImagesDict.images["fontquestion"]
        elif (char == '/'):
            img = ImagesDict.images["fontslash"]
        elif (char == '\\'):
            img = ImagesDict.images["fontbackslash"]
        elif (char == ':'):
            img = ImagesDict.images["fontcolon"]
        elif (char == '*'):
            img = ImagesDict.images["fontstar"]
        elif (char == '"'):
            img = ImagesDict.images["fontdoublequote"]
        elif (char == '|'):
            img = ImagesDict.images["fontpipe"]
        elif (char == '<'):
            img = ImagesDict.images["fontlessthan"]
        elif (char == '>'):
            img = ImagesDict.images["fontmorethan"]
        elif (("font" + char) in ImagesDict.images): # a
            img = ImagesDict.images["font" + char]
        else:
            print ("Cannot find character: ", char)
            img = ImagesDict.images["fontunknown"]
        return img
    def __getLengthOfText (self, string:str) -> int:
        startX = -1 # account for space at the end of the text
        for char in string:
            #if (char >= 'a' and char <= 'z'):
            #    img = ImagesDict.images["font" + char + "2"]
            #elif (char >= 'A' and char <= 'Z'):
            img = self.__getCharImg(char)
            startX += img[0].get_width() + 1 # 1 space in-between characters
        return startX
    
    def setImageText(self, string:str, color:tuple[int, int, int, int]=(0, 0, 0, 255), centered:bool = True)->Self:
        """
        """
        if (string == ""):
            self.setImageName("") # empty
            return self
        name = "TEXT" + ' '.join(map(str, color)) + string # save all copies of colors of strings of text
        if (name) not in ImagesDict.images:
            textSurface = pygame.Surface((self.__getLengthOfText (string), 5), pygame.SRCALPHA)
            
            startX = 0

            for char in string:
                img = self.__getCharImg (char)

                if (color != (0, 0, 0, 255)):
                    copy = img[0].copy() 
                    copy.fill(color, special_flags=pygame.BLEND_MAX)
                else:
                    copy = img[0]

                textSurface.blit (copy, (startX, 0))

                startX += img[0].get_width() + 1
            
            ImagesDict.images [name] = {} 
            ImagesDict.images [name][0] = textSurface
        if (centered):
            self._origin = [0.5, 1]
        else:
            self._origin = [0, 1]
        self.setImageName(name)
        return self
    
    def contains (self, pos:tuple[int, int])->bool:
        frame = self._frame % len(ImagesDict.images[self._imageName])
        left = - self._origin[0] * ImagesDict.images[self._imageName][frame].get_width() - 1
        top = - self._origin[1] * ImagesDict.images[self._imageName][frame].get_height()  - 1 
        right = (1 - self._origin[0]) * ImagesDict.images[self._imageName][frame].get_width() 
        bottom = (1 - self._origin[1]) * ImagesDict.images[self._imageName][frame].get_height() 
        return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)
    
    def assignMouseHover (self, function)->Self:
        self.gm.assignMouseHover(self, function)
        return self
    def assignMouseDown (self, function)->Self:
        self.gm.assignMouseDown(self, function)
        return self
    def assignMouseDrag (self, function)->Self:
        self.gm.assignMouseDrag(self, function)
        return self
    def assignMouseUp (self, function)->Self:
        self.gm.assignMouseUp(self, function)
        return self
    def assignDelete (self, function)->Self:
        self.gm.assignDelete(self, function)
        return self
    def assignKeyPress (self, function)->Self:
        self.gm.assignKeyPress(function)
        return self
    def assignButton (self, buttonname:str, function)->Self:
        self.gm.assignButton(buttonname, function)
        return self

    def deleteSelf (self) -> Self:
        self.gm.removeGameObject(self)
        return self