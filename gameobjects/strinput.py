import math
from gameobject import GameObject
import random
import gamemanager
from typing import Self

class StrInput(GameObject):
    def __init__(self, gm:gamemanager)->None:
        GameObject.__init__(self, gm)
        self.assignKeyPress(self.handleKeyPress)
        self.text = ""
        self.color = (0, 0, 0, 255)
        self.censored = False
        self.mul = math.pow(2, 1.0/12)
    def setCensored (self, censored:bool)->Self:
        self.censored = censored
        return self
    def setColor (self, color:tuple[int, int, int, int])->Self:
        self.color = color
        return self
    def setText (self, text:str)->Self:
        """
        set default text value (for pre-filling)
        """
        self.text = text
        return self
    def tick(self)->None:
        if (self.censored):
            self.setImageText("*"*len(self.text), self.color, False)
        else:
            self.setImageText(self.text, self.color, False)

    def getText (self)->str:
        return self.text
    def handleKeyPress (self, key:str):
        keySound = 0
        if (key.isalnum() and len(key) == 1):
            self.text += key
        elif key == '/': # convert to 'shift' variants automatically
            self.text += '?'
        elif key == '`':
            self.text += '~'
        elif key == ';':
            self.text += ':'
        elif key in ['.', '-', '=', ',', '[', ']', ':', "'", '\\']: # other allowed characters
            self.text += key
        elif key == 'space':
            self.text += ' '
            keySound = 40
        elif key == 'backspace':
            self.text = self.text[:-1]
            keySound = 41
        else:
            keySound = -1
        if (keySound == 0):
            if (key.isalpha()):
                keySound = ord(key) - 32
            else:
                keySound = ord(key)
        if keySound != -1:
            keySound -= 38
            self.playSound(25*math.pow(self.mul, keySound), 46)