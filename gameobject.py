from typing import Callable, Self
import pygame
import pygame.midi
from imagesdict import ImagesDict

class GameObject:
    """An object for use in GameState.
    
    ...
    
    Attributes
    ----------
    queued_child_game_objects : list[GameObject]
        A list of child objects this GameObject created that should be removed
        and added to GameManager's list of GameObjects
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
    on_button : list[(str, Callable[[], None])]
        A list of functions that will be called when the specified button is pressed
    on_delete : list[Callable[[], None]]
        A list of functions that will be called when the GameObject is being deleted
    deleted : bool
        Whether or not this GameObject should be scheduled for deletion
    """
    midi_out: pygame.midi.Output = None

    def __init__(self, pos:tuple[int, int]=(0, 0), origin:tuple[int, int]=(0.5, 1))->None:
        self._origin = origin

        self._muted = False
        self._pos = None
        self._next_pos = pos
        self._image_name = ""
        self._frames_per_frame = 1
        self._frame = 0
        self._mirrored = False
        self.__last_played = (0, 0)

        self.queued_child_game_objects:list[GameObject] = []

        self.on_mouse_hover:list[Callable[[],None]] = []
        self.on_mouse_down:list[Callable[[],None]] = []
        self.on_mouse_drag:list[Callable[[],None]] = []
        self.on_mouse_up:list[Callable[[],None]] = []
        self.on_key_press:list[Callable[[str],None]] = []
        self.on_button:list[(str, Callable[[],None])] = []
        self.on_delete:list[Callable[[],None]] = []

        self.on_delete.append(self.__delete_sound)
        self.deleted = False

    def add_child_object(self, go:Self)->Self:
        """This function queues the GameObject to be added to the game manager's list of objects

        Parameters:
            go : GameObject
                The GameObject to be added to the game manager's list of objects
        Return:
            The child GameObject
        """
        self.queued_child_game_objects.append(go)
        return go

    def set_muted (self, muted:bool)->Self:
        """Set the mute state of this GameObject.
        
        Parameters:
            go : bool
                Whether or not this GameObject should be muted
        Return:
            self
        """
        if muted:
            self.__delete_sound()
        self._muted = muted
        return self

    def __delete_sound(self)->None:
        self.midi_out.note_off(*self.__last_played)

    def set_frames_per_frame (self, frames:int)->Self:
        """Set the animation speed of this GameObject.
        
        Parameters:
            frames : int
                The number of frames each image in the animation should last for.
                1 = every frame, the image should change = 5fps
                2 = every 2 frames, the image should change = 2.5fps
                5 = every 5 frames, the image should change = 1fps
                While a float is accepted, the game runs strictly at 5fps, which may cause stutters.
        Return:
            self
        """
        self._frames_per_frame = 1.0/frames
        return self
    def _get_frame (self)->int:
        """Get the current frame of this GameObject.
        
        Return:
            int
                The frame of this GameObject that will be drawn to the screen
        """
        return int(self._frame)

    def tick(self)->None:
        """Derived classes may override this function. 
        This function is called each game tick.
        """

    def _mirror(self)->Self:
        """Mirror this GameObject in the next draw call.
        
        Return:
            self
        """
        self._mirrored = True
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
        ImagesDict.draw_image(self._image_name, self._pos, self._origin, self._get_frame(), self._mirrored)
        self._frame += self._frames_per_frame
        self._mirrored = False

    def set_origin (self, origin:tuple[int, int])->Self:
        """Set the origin of this GameObject.
        
        Parameters:
            origin : tuple[int, int]
                The origin this GameObject should have
        Return:
            self
        """
        self._origin = origin
        return self
    def get_pos(self)->tuple[int, int]:
        """Get this GameObject's position.

        Return:
            tuple[int, int]
                This GameObject's position
        """
        if self._pos is None: # if hasn't been initialized yet
            self._pos = self._next_pos
        return self._pos
    def set_pos(self, pos:tuple[int, int])->Self:
        """Set this GameObject's position.

        Parameters:
            pos : tuple[int, int]
                The position this GameObject should be set to
        Return:
            self
        """
        self._next_pos = pos
        return self

    def _play_sound (self, note:int, instrument:int=1, volume:int=100)->None:
        """Have this GameObject play a sound. 
        The sound is stopped when this GameObject play another sound, or is deleted.
        
        Parameters:
            note : int
                The note that should be played (0-127)
            instrument : int
                The MIDI instrument to be used (0-127)
            volume : 
                How loud this sound should be played (0-127)
        """
        if not self._muted:
            self.midi_out.note_off(*self.__last_played)
            self.midi_out.set_instrument(instrument)
            self.__last_played = (note, volume)
            self.midi_out.note_on(*self.__last_played)


    def set_image_name(self, name:str)->Self:
        """The name of the image / animation this GameObject should have.
        The name must correspond to a file or set of files in the "images/" folder.

        Parameters:
            name : str
                The name of the image / animation
        Return:
            self
        """
        if name != self._image_name:
            self._image_name = name
            self._frame = 0 # reset animation state on name change
        return self

    def __get_char_img (self, char:str)-> pygame.Surface:
        if char >= 'a' and char <= 'z':
            char = char.upper()
        if char >= 'A' and char <= 'Z':
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
            print ("Cannot find character: ", char)
            img = ImagesDict.images["fontunknown"]
        return img
    def __get_length_of_text (self, string:str) -> int:
        start_x = -1 # account for extra space at the end of the text
        for char in string:
            img = self.__get_char_img(char)
            start_x += img[0].get_width() + 1 # 1 space in-between characters
        return start_x

    def set_image_text(self, string:str, color:tuple[int, int, int, int]=(0, 0, 0, 255))->Self:
        """Set this GameObject image to a string of text. This uses the "font" images.

        Parameters:
            string : str
                The text to display
            color : tuple[int, int, int, int]
                The color the text should be
        Return:
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
        
        Parameters:
            pos : tuple[int, int]
                The position to check
        Return:
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

        Parameters:
            buttonname : str
                The button to listen for.
                Alphanumerics are alphanumerics
                The 'enter' button is "return"
                The 'spacebar' is "space"
        Return:
            self
        """
        self.on_button.append((buttonname, function))
        return self

    def set_deleted (self, deleted:bool=True) -> Self:
        """Queue this GameObject for destruction by the GameManager.
        
        Parameters:
            deleted : bool
                Whether or not this GameObject should be queued for destruction
        Return:
            self
        """
        self.deleted = deleted
        return self
