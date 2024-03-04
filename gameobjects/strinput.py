from typing import Self
from gameobject import GameObject

class StrInput(GameObject):
    """Easily create a string input text box with the StrInput class
    
    ...

    Attributes
    ----------
    text : str
        The text that is currently in this StrInput
    char_limit : int
        The maximum number of characters that can be entered into this StrInput
    """
    def __init__(self)->None:
        GameObject.__init__(self)
        self.on_key_press.append(self._handle_key_press)
        self.text = ""
        self._color = (0, 0, 0, 255)
        self._censored = False
        self._cursor_frame_cnt = 0
        self._cursor_on = True
        self.set_origin((0, 1))

        self.char_limit = 12
    def set_censored (self, censored:bool)->Self:
        """Set if all text should appear as '*'s (for password inputs).
        Also makes all keys sound the same.
        
        Parameters:
            censored : bool
                If the text should be censored
        Return:
            self
        """
        self._censored = censored
        return self
    def set_color (self, color:tuple[int, int, int, int])->Self:
        """Sets the color of the text.
        
        Parameters:
            color : tuple[int, int, int, int]
                The color to set this text to
        Return:
            self
        """
        self._color = color
        return self
    def set_text (self, text:str)->Self:
        """Set initial text value.

        Parameters:
            text : str
                The text the StrInput should start with
        Return:
            self
        """
        self.text = text
        return self
    def set_char_limit (self, maximum:int)->Self:
        """Sets the character limit for this StrInput.

        Parameters:
            maximum : int
                The maximum number of characters
        """
        self.char_limit = maximum
        return self
    def tick(self)->None:
        if self._censored:
            if self._cursor_on:
                self.set_image_text("*"*len(self.text) + "_", self._color)
            else:
                self.set_image_text("*"*len(self.text), self._color)
        else:
            if (self._cursor_on and len(self.text) < self.char_limit):
                self.set_image_text(self.text + "_", self._color)
            else:
                self.set_image_text(self.text, self._color)
        self._cursor_frame_cnt += 1
        if self._cursor_frame_cnt >= 3:
            self._cursor_on = not self._cursor_on
            self._cursor_frame_cnt = 0

    def get_text (self)->str:
        """Get the text currently in this StrInput.
        
        Return:
            str
                The text in this StrInput
        """
        return self.text
    def _handle_key_press (self, key:str):
        key_sound = 0
        if len(self.text) < self.char_limit:
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
        if key_sound == 0:
            if key.isalpha():
                key_sound = ord(key) - 32
            else:
                key_sound = ord(key)
        if key_sound != -1:
            if self._censored:
                if key == 'backspace':
                    key_sound = 41
                else:
                    key_sound = 60
            self._play_sound(127 - key_sound, 45)
