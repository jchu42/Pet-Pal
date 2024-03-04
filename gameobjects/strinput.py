import math
from gameobject import GameObject
import random
import gamemanager
from typing import Self

class StrInput(GameObject):
    def __init__(self)->None:
        GameObject.__init__(self)
        self.on_key_press.append(self.handle_key_press)
        self.text = ""
        self.color = (0, 0, 0, 255)
        self.censored = False
        self.mul = math.pow(2, 1.0/12)
        self.cursor_frame_cnt = 0
        self.cursor_on = True

        self.CHAR_LIMIT = 12
    def set_censored (self, censored:bool)->Self:
        self.censored = censored
        return self
    def set_color (self, color:tuple[int, int, int, int])->Self:
        self.color = color
        return self
    def set_text (self, text:str)->Self:
        """
        set default text value (for pre-filling)
        """
        self.text = text
        return self
    def tick(self)->None:
        if (self.censored):
            if (self.cursor_on):
                self.set_image_text("*"*len(self.text) + "_", self.color, False)
            else:
                self.set_image_text("*"*len(self.text), self.color, False)
        else:
            if (self.cursor_on and len(self.text) < self.CHAR_LIMIT):
                self.set_image_text(self.text + "_", self.color, False)
            else:
                self.set_image_text(self.text, self.color, False)
        self.cursor_frame_cnt += 1
        if (self.cursor_frame_cnt >= 3):
            self.cursor_on = not self.cursor_on
            self.cursor_frame_cnt = 0

    def get_text (self)->str:
        return self.text
    def handle_key_press (self, key:str):
        key_sound = 0
        if (len(self.text) < self.CHAR_LIMIT):
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
                key_sound = 40
            else:
                key_sound = -1
        else:
            key_sound = -1
        if key == 'backspace':
            self.text = self.text[:-1]
            key_sound = 41
        if (key_sound == 0):
            if (key.isalpha()):
                key_sound = ord(key) - 32
            else:
                key_sound = ord(key)
        if key_sound != -1:
            key_sound -= 38
            if (self.censored):
                key_sound = 60
            if key == 'backspace':
                key_sound = 41
            self.play_sound(25*math.pow(self.mul, key_sound), 46)