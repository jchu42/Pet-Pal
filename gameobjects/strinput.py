"""This module contains the StrInput class which is used to create a textbox for user input"""
from typing import Self
from gameobject import GameObject
from exceptions import KeyException

BACKSPACE_DURATION_DELETE_ALL = 3

class StrInput(GameObject):
    """Easily create a string input text box with the StrInput class
    
    ...

    Attributes
    ----------
    text : str
        The text that is currently in this StrInput
    _color : tuple[int, int, int, int]
        The color of this StrInputs text
    _censored : bool
        Whether or not all input in this StrInput should be *, and all sound sound the same
    _cursor_frame_cnt : int
        Used to keep track of how many frames the cursor's current state has been active for
    _cursor_on : bool
        Whether or not the cursor is currently active
    char_limit : int
        The maximum number of characters that can be entered into this StrInput
    _shift_pressed : bool
        Whether or not the shift button is currently being pressed
    _backspace_held : bool
        Whether or not the backspace button us currently being pressed
    _backspace_duration : int
        How long the backspace button has been pressed for
    """
    def __init__(self,
                 color:tuple[int, int, int, int]=(0, 0, 0, 255),
                 initial_text = "",
                 censored=False,
                 origin:tuple[float, float]=(0, 1),
                 **wargs)->None:
        """Initialize the StrInput class
        
        Parameters
        ----------
        color : tuple[int, int, int, int], default=(0, 0, 0, 255)
            The color of the text in this StrInput
        initial_text : str, default=""
            The text this StrInput should start with
        censored : bool, default=False
            Whether or not all input in this textbox should appear as *, and sound all the same
        origin : tuple[float, float], default=(0, 1)
            The origin this StrInput should have
        """
        GameObject.__init__(self, origin=origin, **wargs)
        self.on_key_press.append(self._handle_key_press)
        self.on_key_release.append(self._handle_key_release)
        self.text = initial_text
        self._color = color
        self._censored = censored
        self._cursor_frame_cnt = 0
        self._cursor_on = True

        self.char_limit = 12
        self._shift_pressed = False
        self._backspace_held = False
        self._backspace_duration = 0
    def set_censored (self, censored:bool)->Self:
        """Set if all text should appear as '*'s (for password inputs).
        Also makes all keys sound the same.
        
        Parameters
        ----------
        censored : bool
            If the text should be censored

        Returns
        -------
        StrInput
            self
        """
        self._censored = censored
        return self
    def set_color (self, color:tuple[int, int, int, int])->Self:
        """Sets the color of the text.
        
        Parameters
        ----------
        color : tuple[int, int, int, int]
            The color to set this text to

        Returns
        -------
        StrInput
            self
        """
        self._color = color
        return self
    def set_text (self, text:str)->Self:
        """Set initial text value.

        Parameters
        ----------
        text : str
            The text the StrInput should start with

        Returns
        -------
        StrInput
            self
        """
        self.text = text
        return self
    def set_char_limit (self, maximum:int)->Self:
        """Sets the character limit for this StrInput.

        Parameters
        ----------
        maximum : int
            The maximum number of characters

        Returns
        -------
        StrInput
            self
        """
        self.char_limit = maximum
        return self
    def tick(self)->None:
        """Update text, animate "_" cursor icon, and trigger backspace hold action"""
        if self._censored:
            if self._cursor_on:
                self.set_image_text("*"*len(self.text) + "_", self._color)
            else:
                self.set_image_text("*"*len(self.text) + " ", self._color)
        else:
            if (self._cursor_on and len(self.text) < self.char_limit):
                self.set_image_text(self.text + "_", self._color)
            else:
                self.set_image_text(self.text + " ", self._color)
        self._cursor_frame_cnt += 1
        if self._cursor_frame_cnt >= 3:
            self._cursor_on = not self._cursor_on
            self._cursor_frame_cnt = 0
        if self._backspace_held:
            self._backspace_duration += 1
            if self._backspace_duration > BACKSPACE_DURATION_DELETE_ALL:
                self.text = ""
                self._backspace_held = False
                self._backspace_duration = 0
                self.queue_sound(10)

    def get_text (self)->str:
        """Get the text currently in this StrInput.
        
        Returns
        -------
        str
            The text in this StrInput
        """
        return self.text
    def _handle_key_press (self, key:str)->None:
        """Add the buttons pressed by the user to this StrInput's 'text'
        
        Parameters
        ----------
        key : str
            The button that was pressed by the user
        """
        key_sound = 0
        if key in ('left shift', 'right shift'):
            self._shift_pressed = True
            return
        elif key == 'backspace':
            self.text = self.text[:-1]
            key_sound = 41
            self._backspace_held = True
        elif len(self.text) >= self.char_limit:
            return
        elif key in ("return", "escape", "tab"):
            return
        elif (key.isalnum() and len(key) == 1):
            if self._shift_pressed:
                if key.isalpha():
                    self.text += key.upper()
                else:
                    match key:
                        case '1':
                            self.text += "!"
                        case '2':
                            self.text += "@"
                        case '3':
                            self.text += "#"
                        case '4':
                            self.text += "$"
                        case '5':
                            self.text += "%"
                        case '6':
                            self.text += "^"
                        case '7':
                            self.text += "&"
                        case '8':
                            self.text += "*"
                        case '9':
                            self.text += "("
                        case '0':
                            self.text += ")"
                key_sound = ord(key)
            else:
                self.text += key
                key_sound = ord(key) - 30
        elif len(key) == 1:
            if self._shift_pressed:
                match key:
                    case '`':
                        self.text += "~"
                    case '-':
                        self.text += "_"
                    case '=':
                        self.text += "+"
                    case '[':
                        self.text += "{"
                    case ']':
                        self.text += "}"
                    case '\\':
                        self.text += "|"
                    case ";":
                        self.text += ":"
                    case "'":
                        self.text += '"'
                    case "/":
                        self.text += "?"
                    case ",":
                        self.text += "<"
                    case ".":
                        self.text += ">"
                    case _:
                        raise KeyException("Oops; key not found 2. key pressed =" + key)
                key_sound = ord(key)
            else:
                self.text += key
                key_sound = ord(key) - 30
        elif key == 'space':
            self.text += ' '
            key_sound = 40
        else:
            return #raise KeyException("Oops; key not found. key pressed =" + key)

        if self._censored:
            if key == 'backspace':
                key_sound = 41
            else:
                key_sound = 60
        self.queue_sound(127 - key_sound, 45)
    def _handle_key_release (self, key:str)->None:
        """Toggle shift and/or backspace key as off when released
        
        Parameters
        ----------
        key : str
            The button that was released
        """
        if key in ('left shift', 'right shift'):
            self._shift_pressed = False
        if key == "backspace":
            self._backspace_held = False
            self._backspace_duration = 0