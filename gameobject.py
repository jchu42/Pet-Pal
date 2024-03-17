"""This module contains the GameObject class for use in GameState."""
from typing import Callable, Self
import pygame
import pygame.midi
from imagesdict import ImagesDict
from exceptions import CharNotFoundException

class GameObject:
    """An object for use in GameState.
    
    ...
    
    Attributes
    ----------
    midi_out : pygame.midi.Output, default=None
        Statis object used to play sounds by the GameObject. Requires initialization.
    _muted : bool
        Whether or not this GameObject's sounds shouold be muted
    _next_pos : tuple[int, int]
        The position this GameObject is queued to be in this frame
        Reduces 'first added' bias when comparing object positions with each other during ticks
    _pos : tuple[int, int]
        This GameObject's position in the GameState when drawn
    _origin : tuple[float, float]
        This GameObject's image 'zoro' point
    _image_name : str
        The image name this references in ImagesDict
    _frames_per_frame : int
        The number of frames each frame if exists) of this GameObject should last for
    _frame : int
        The current frame of this GameObject (if current image is animated)
    _mirrored : bool
        If this GameObject's image should be flipped
    queued_child_game_objects : list[GameObject]
        A list of child objects this GameObject created that should be removed
        and added to GameState's list of GameObjects
    queued_sounds : list[tuple[int, int, int, int]]
        A list of sound parameters that have been queued to be played
    __last_instrument
        The last instrument that was played by this GameObject
    on_mouse_hover : list[Callable[[], None]]
        A list of functions that will be called when the mouse hovers over it
    on_mouse_down : list[Callable[[], None]]
        A list of functions that will be called when the mouse clicks down on it
    on_mouse_up : list[Callable[[], None]]
        A list of functions that will be called when the mouse clicks up on it
    on_mouse_drag : list[Callable[[], None]]
        A list of functions that will be called when the mouse is dragged on it
    on_key_press : list[Callable[[str], None]]
        A list of functions that will be called when any keyboard button is pressed. 
        The keyboard button that was pressed will be passed into the function. 
    on_key_release : list[Callable[[str], None]]
        A list of functions that will be called when any keyboard button is released. 
        The keyboard button that was released will be passed into the function. 
    on_button : list[(str, Callable[[], None])]
        A list of functions that will be called when the specified button is pressed
    on_delete : list[Callable[[], None]]
        A list of functions that will be called when the GameObject is being deleted
    deleted : bool
        Whether or not this GameObject should be scheduled for deletion
    """
    midi_out: pygame.midi.Output = None

    def __init__(self,
                 imagename:str="",
                 imagetext:tuple[str, tuple[int, int, int, int]]|tuple[str]=("", (0, 0, 0, 255)),
                 layer:int=3,
                 pos:tuple[int, int]=(0, 0),
                 origin:tuple[float, float]=(0.5, 1),
                 muted:bool=False,
                 # https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/dangerous-default-value.html
                 on_mouse_hover:list[Callable[[], None]]=None,
                 on_mouse_down:list[Callable[[], None]]=None,
                 on_mouse_drag:list[Callable[[], None]]=None,
                 on_mouse_up:list[Callable[[], None]]=None,
                 on_key_press:list[Callable[[str], None]]=None,
                 on_key_release:list[Callable[[str], None]]=None,
                 on_button:list[tuple[str, Callable[[], None]]]=None,
                 on_delete:list[Callable[[], None]]=None
                 )->None:
        """Initialize this GameObject.
        
        Parameters
        ----------
        imagename : str, default=""
            The name of the image to use. If empty, imagetext is used instead.
        imagetext : tuple[str, tuple[int, int, int, int]]
            Only used if imagename is empty. 
            Sets the text to str, and the color of the text to the tuple (rgba).
        layer : int
            The layer to draw this GameObject on. May be negative. 
        pos : tuple[int, int], default=(0, 0)
            The position this GameObject should be when initialized
        origin : tuple[float, float], default=(0.5, 1)
            The origin of the position this GameObejct should have
        muted : bool, default=False
            Whether or not this GameObject should be muted
        on_mouse_hover : list[Callable[[], None]], default=[]
            Functions to add to the mouse hover event
        on_mouse_down : list[Callable[[], None]], default=[]
            Functions to add to the mouse down event
        on_mouse_drag : list[Callable[[], None]], default=[]
            Functions to add to the mouse drag event
        on_mouse_up : list[Callable[[], None]], default=[]
            Functions to add to the mouse up event
        on_key_press : list[Callable[[str], None]], default=[]
            Functions to add to the key press event
        on_key_release : list[Callable[[str], None]], default=[]
            Functions to add to the key release event
        on_button : list[tuple[str, Callable[[], None]]], default=[]
            Functions to add to a button press event
        on_delete : list[Callable[[], None]], default=[]
            Functions to add to call when this GameObject is deleted
        """

        self._muted = muted
        self._pos = None
        self.layer = layer
        self.set_pos(pos)
        self.set_origin(origin)
        self._image_name = ""
        if imagename == "":
            if isinstance(imagetext, str):
                self.set_image_text(imagetext)
            else:
                self.set_image_text(*imagetext)
        else:
            self.set_image_name(imagename)
        self._frames_per_frame = 1
        self._frame = 0
        self._mirrored = False

        self.queued_child_game_objects:list[GameObject] = []

        self.queued_sounds:list[tuple[int, int, int, int]] = []
        self.__last_instrument:int = -1

        self.on_mouse_hover:list[Callable[[],None]] = []
        if on_mouse_hover is not None:
            self.on_mouse_hover.extend(on_mouse_hover)
        self.on_mouse_down:list[Callable[[],None]] = []
        if on_mouse_down is not None:
            self.on_mouse_down.extend(on_mouse_down)
        self.on_mouse_drag:list[Callable[[],None]] = []
        if on_mouse_drag is not None:
            self.on_mouse_drag.extend(on_mouse_drag)
        self.on_mouse_up:list[Callable[[],None]] = []
        if on_mouse_up is not None:
            self.on_mouse_up.extend(on_mouse_up)
        self.on_key_press:list[Callable[[str],None]] = []
        if on_key_press is not None:
            self.on_key_press.extend(on_key_press)
        self.on_key_release:list[Callable[[str],None]] = []
        if on_key_release is not None:
            self.on_key_release.extend(on_key_release)
        self.on_button:list[tuple[str, Callable[[],None]]] = []
        if on_button is not None:
            self.on_button.extend(on_button)
        self.on_delete:list[Callable[[],None]] = []
        if on_delete is not None:
            self.on_delete.extend(on_delete)

        self.on_delete.append(self.__delete_sound)
        self.deleted = False

    def add_child_object(self, go:Self)->Self:
        """This function queues the GameObject to be added to the game manager's list of objects

        Parameters
        ----------
        go : GameObject
            The GameObject to be added to the game manager's list of objects

        Returns
        -------
        GameObject
            The child GameObject
        """
        self.queued_child_game_objects.append(go)
        return go

    def set_muted (self, muted:bool = True)->Self:
        """Set the mute state of this GameObject.
        
        Parameters
        ----------
        go : bool, default=True
            Whether or not this GameObject should be muted

        Returns
        -------
        GameObject
            self
        """
        if muted:
            self.__delete_sound()
        self._muted = muted
        return self

    def __delete_sound(self)->None:
        """Turns off the last played MIDI note."""
        if len(self.queued_sounds) > 0:
            self.midi_out.note_off(self.queued_sounds[0][0], self.queued_sounds[0][2])

    def set_frames_per_frame (self, frames:int)->Self:
        """Set the animation speed of this GameObject.
        
        Parameters
        ----------
        frames : int
            The number of frames each image in the animation should last for.
            1 = every frame, the image should change = 5fps
            2 = every 2 frames, the image should change = 2.5fps
            5 = every 5 frames, the image should change = 1fps
            While a float is accepted, the game runs strictly at 5fps, which may cause stutters.

        Returns
        -------
        GameObject
            self
        """
        self._frames_per_frame = 1.0/frames
        return self
    def _num_frames(self)->int:
        """Get the number of frames for the current image
        
        Returns
        -------
        int
            Number of frames in the current image
        """
        return len(ImagesDict.images[self._image_name])
    def _get_frame (self)->int:
        """Get the current frame of this GameObject.
        
        Returns
        -------
        int
            The frame of this GameObject that will be drawn to the screen
        """
        return int(self._frame)

    def tick(self)->None:
        """Derived classes may override this function. 
        This function is called each game tick.
        """

    def _mirror(self, mirror:bool)->Self:
        """Mirror this GameObject in the next draw call.
        
        Parameters
        ----------
        mirror : bool
            Whether or not to mirror this GameObject

        Returns
        -------
        GameObject
            self
        """
        self._mirrored = mirror
        return self
    def draw(self)->None:
        """Use internal variables to draw this object.

        Call set_image_name(str) or set_image_text(str) to set the image
        Call set_pos(tuple[int, int]) to set the position
        Call set_origin(tuple[int, int]) to set the origin
        Call _mirror() to mirror the image horizontally
        Call _set_frames_per_frame(int) to slow the animation speed
        Call _get_frame() to get the current frame of the animation
        """
        self._pos = self._next_pos
        ImagesDict.draw_image(self._image_name, self._pos,
                              self._origin, self._get_frame(), self._mirrored)
        self._frame += self._frames_per_frame

    def set_origin (self, origin:tuple[float, float])->Self:
        """Set the origin of this GameObject.
        
        Parameters
        ----------
        origin : tuple[float, float]
            The origin this GameObject should have

        Returns
        -------
        GameObject
            self
        """
        self._origin = origin
        return self
    def get_pos(self)->tuple[int, int]:
        """Get this GameObject's position.

        Returns
        -------
        tuple[int, int]
            This GameObject's position
        """
        if self._pos is None: # if hasn't been initialized yet
            self._pos = self._next_pos
        return self._pos
    def set_pos(self, pos:tuple[int, int])->Self:
        """Set this GameObject's position.

        Parameters
        ----------
        pos : tuple[int, int]
            The position this GameObject should be set to

        Returns
        -------
        GameObject
            self
        """
        self._next_pos = pos
        return self

    def queue_sound (self, note:int, instrument:int=1, volume:int=100, duration:int=1)->None:
        """Have this GameObject queue a sound to play. 
        The sound is stopped when this GameObject play another sound, or is deleted.
        
        Parameters
        ----------
        note : int
            The note that should be played (0-127)
        instrument : int
            The MIDI instrument to be used (0-127)
        volume : 
            How loud this sound should be played (0-127)
        """
        if not self._muted:
            self.queued_sounds.append((note, instrument, volume, duration))

    def play_sound (self)->None:
        """Play the next queued MIDI note"""
        if len(self.queued_sounds) > 0:
            note, instrument, volume, duration = self.queued_sounds[0]
            if duration <= 0:
                self.midi_out.note_off(note, volume)
                self.queued_sounds.pop(0)
            if len(self.queued_sounds) > 0:
                note, instrument, volume, duration = self.queued_sounds[0]
                self.queued_sounds[0] = (note, instrument, volume, duration - 1)
                if self.__last_instrument != instrument:
                    self.midi_out.set_instrument(instrument)
                    self.__last_instrument = instrument
                self.midi_out.note_on(note, volume)
            else:
                self.__last_instrument = -1

    def set_image_name(self, name:str)->Self:
        """The name of the image / animation this GameObject should have.
        The name must correspond to a file or set of files in the "images/" folder.

        Parameters
        ----------
        name : str
            The name of the image / animation

        Returns
        -------
        GameObject
            self
        """
        if name != self._image_name:
            self._image_name = name
            self._frame = 0 # reset animation state on name change
        return self

    def __get_char_img (self, char:str)-> pygame.Surface:
        """Get the image from ImageDict of the corresponding character.
        
        Parameters
        ----------
        char : str
            The character to get the image of
        
        Returns
        -------
        pygame.Surface
            The image of the character

        Raises
        ------
        CharNotFoundException
            If the font character(s) is not found in ImagesDict
        """
        if char >= 'a' and char <= 'z':
            img = ImagesDict.images["font" + char + "2"]
        elif char >= 'A' and char <= 'Z':
            img = ImagesDict.images["font" + char]
        elif char == ".":
            img = ImagesDict.images["fontdot"]
        elif char == "?":
            img = ImagesDict.images["fontquestion"]
        elif char == '/':
            img = ImagesDict.images["fontslash"]
        elif char == '\\':
            img = ImagesDict.images["fontbackslash"]
        elif char == ':':
            img = ImagesDict.images["fontcolon"]
        elif char == '*':
            img = ImagesDict.images["fontstar"]
        elif char == '"':
            img = ImagesDict.images["fontdoublequote"]
        elif char == '|':
            img = ImagesDict.images["fontpipe"]
        elif char == '<':
            img = ImagesDict.images["fontlessthan"]
        elif char == '>':
            img = ImagesDict.images["fontmorethan"]
        elif "font" + char in ImagesDict.images:
            img = ImagesDict.images["font" + char]
        else:
            raise CharNotFoundException ("Cannot find character: ", char)
        return img
    def __get_length_of_text (self, string:str) -> int:
        """Get the number of pixels that the input string would take to display.
        
        Parameters
        ----------
        string : str
            The string of text to use
        
        Returns
        -------
        int
            The number of pixels
        """
        start_x = -1 # account for extra space at the end of the text
        for char in string:
            img = self.__get_char_img(char)
            start_x += img[0].get_width() + 1 # 1 space in-between characters
        return start_x

    def set_image_text(self, string:str, color:tuple[int, int, int, int]=(0, 0, 0, 255))->Self:
        """Set this GameObject image to a string of text. This uses the "font" images.

        Parameters
        ----------
        string : str
            The text to display
        color : tuple[int, int, int, int]
            The color the text should be

        Returns
        -------
        GameObject
            self
        """
        if string == "":
            self.set_image_name("") # empty
            return self
        name = "TEXT" + ' '.join(map(str, color)) + string
        if name not in ImagesDict.images: # save all copies of colors of strings of text
            text_surface = pygame.Surface((self.__get_length_of_text (string), 5), pygame.SRCALPHA)

            start_x = 0
            for char in string:
                img = self.__get_char_img (char)
                if color != (0, 0, 0, 255):
                    copy = img[0].copy() 
                    copy.fill(color, special_flags=pygame.BLEND_MAX)
                else:
                    copy = img[0]
                text_surface.blit (copy, (start_x, 0))
                start_x += img[0].get_width() + 1

            ImagesDict.images [name] = {}
            ImagesDict.images [name][0] = text_surface
        self.set_image_name(name)
        return self

    def contains (self, pos:tuple[int, int])->bool:
        """Check if the position is within the square of the image of this GameObject.
        
        Parameters
        ----------
        pos : tuple[int, int]
            The position to check

        Returns
        -------
        bool
            Whether or not the point is contained in thie GameObject's space
        """
        if self._image_name not in ImagesDict.images:
            return False
        frame = self._get_frame() % len(ImagesDict.images[self._image_name])
        left = - self._origin[0] * ImagesDict.images[self._image_name][frame].get_width() - 1
        top = - self._origin[1] * ImagesDict.images[self._image_name][frame].get_height()  - 1 
        right = (1 - self._origin[0]) * ImagesDict.images[self._image_name][frame].get_width() 
        bottom = (1 - self._origin[1]) * ImagesDict.images[self._image_name][frame].get_height() 
        return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)

    def assign_button (self, buttonname:str, function)->Self:
        """Add a button function for the corresponding button.

        Parameters
        ----------
        buttonname : str
            The button to listen for.
            Alphanumerics are alphanumerics
            The 'enter' button is "return"
            The 'spacebar' is "space"

        Returns
        -------
        GameObject
            self
        """
        self.on_button.append((buttonname, function))
        return self

    def set_deleted (self, deleted:bool=True) -> Self:
        """Queue this GameObject for destruction by the GameManager.
        
        Parameters
        ----------
        deleted : bool
            Whether or not this GameObject should be queued for destruction

        Returns
        -------
        GameObject
            self
        """
        self.deleted = deleted
        return self
