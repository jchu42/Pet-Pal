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
    def setColor (self, color:tuple[int, int, int, int])->Self:
        self.color = color
        return self
    
    def tick(self)->None:
        self.setImageText(self.text, self.color, False)

    def getText (self)->str:
         return self.text
    def handleKeyPress (self, go:GameObject, key:str):
        print (key)
        if (key.isalnum() and len(key) == 1):
            # if (shiftHeld):
            #     textDebugString += key.capitalize()
            # else:
            self.text += key
        #elif shiftHeld and key in ['/']:
        elif key == '/':
            self.text += '?'
        elif key == '`':
            self.text += '~'
        elif key == '\\':
            self.text += '\\'
        elif key in ['.', '-', '=', ',', '[', ']', ':', "'"]:
            self.text += key
        elif key == 'space':
            self.text += ' '
        # elif key == 'left shift' or key == 'right shift':
        #     shiftHeld = True
        elif key == 'backspace':
            self.text = self.text[:-1]
