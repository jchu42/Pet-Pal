from gameobject import GameObject
import random
import gamemanager
from typing import Self

textDebug = False

class StrInput(GameObject):
    def __init__(self, gm:gamemanager)->None:
        GameObject.__init__(self, gm)
        self.assignKeyPress(self.handleKeyPress)
        self.text = ""
        self.color = (0, 0, 0, 255)
        self.censored = False
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
        elif key == 'backspace':
            self.text = self.text[:-1]
        # ignore other key presses

        if (textDebug):
            print (key, self.text)
