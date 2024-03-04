from typing import Callable, Self
import time
import gamemanager
from imagesdict import ImagesDict
import pygame

class GameObject:

    midi_out: pygame.midi.Output = None

    def __init__(self, origin:tuple[int, int]=(0.5, 0.5))->None:
        # self.gm = gm
        # gm.add_game_object(self)
        self._origin = origin

        self._muted = False
        self._pos = None
        self._next_pos = (0, 0)
        self._image_name = ""
        self._frames_per_frame = 1
        self._frame = 0
        self._mirrored = False
        self.last_played = (0, 0)

        self.queued_child_game_objects:list[GameObject] = []

        self.on_mouse_hover:list[Callable[[],None]] = []
        self.on_mouse_down:list[Callable[[],None]] = []
        self.on_mouse_drag:list[Callable[[],None]] = []
        self.on_mouse_up:list[Callable[[],None]] = []
        self.on_key_press:list[Callable[[str],None]] = []
        self.on_button:list[Callable[[],None]] = []
        self.on_delete:list[Callable[[],None]] = []

        self.on_delete.append(self.__delete_sound)
        self.deleted = False

    def add_child_object(self, go:Self)->Self:
        """This function queues the game objects to be added to the game manager's list of objects"""
        self.queued_child_game_objects.append(go)
        return go

    def set_muted (self, muted:bool)->Self:
        self._muted = muted
        return self

    def __delete_sound(self)->None:
        self.midi_out.note_off(*self.last_played)

    def set_frames_per_frame (self, frames:int)->Self:
        self._frames_per_frame = 1.0/frames
        return self
    def get_frame (self)->int:
        return int(self._frame)

    def tick(self)->None:
        pass

    def mirror(self)->Self:
        self._mirrored = True
        return self
    def draw(self)->None:
        self._pos = self._next_pos
        ImagesDict.draw_image(self._image_name, self._pos, self._origin, self.get_frame(), self._mirrored)
        self._frame += self._frames_per_frame
        self._mirrored = False
    def set_origin (self, origin:tuple[int, int])->Self:
        self._origin = origin
        return self
    def get_pos(self)->tuple[int, int]:
        if (self._pos == None): # if hasn't been initialized yet
            self._pos = self._next_pos
        return self._pos
    def set_pos(self, pos:tuple[int, int])->Self:
        self._next_pos = pos
        return self
    
    def play_sound (self, frequency:int, instrument:int=1, volume:int=100):#, duration:int=2):
        if not self._muted:
            self.midi_out.note_off(*self.last_played) 
            self.midi_out.set_instrument(instrument)
            self.last_played = (pygame.midi.frequency_to_midi(frequency), volume)
            self.midi_out.note_on(*self.last_played) 


    def set_image_name(self, name:str)->Self:
        if (name != self._image_name):
            self._image_name = name
            self._frame = 0 # reset animation state on name change
        return self

    def __get_char_img (self, char:str)-> pygame.Surface:
        if (char >= 'a' and char <= 'z'):
            char = char.upper()
        if (char >= 'A' and char <= 'Z'):
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
            img = self.__get_char_img(char)
            startX += img[0].get_width() + 1 # 1 space in-between characters
        return startX
    
    def set_image_text(self, string:str, color:tuple[int, int, int, int]=(0, 0, 0, 255), centered:bool = True)->Self:
        """
        """
        if (string == ""):
            self.set_image_name("") # empty
            return self
        name = "TEXT" + ' '.join(map(str, color)) + string # save all copies of colors of strings of text
        if (name) not in ImagesDict.images:
            text_surface = pygame.Surface((self.__getLengthOfText (string), 5), pygame.SRCALPHA)
            
            start_x = 0

            for char in string:
                img = self.__get_char_img (char)

                if (color != (0, 0, 0, 255)):
                    copy = img[0].copy() 
                    copy.fill(color, special_flags=pygame.BLEND_MAX)
                else:
                    copy = img[0]

                text_surface.blit (copy, (start_x, 0))

                start_x += img[0].get_width() + 1
            
            ImagesDict.images [name] = {} 
            ImagesDict.images [name][0] = text_surface
        if (centered):
            self._origin = [0.5, 1]
        else:
            self._origin = [0, 1]
        self.set_image_name(name)
        return self
    
    def contains (self, pos:tuple[int, int])->bool:
        if (self._image_name not in ImagesDict.images):
            return False
        frame = self.get_frame() % len(ImagesDict.images[self._image_name])
        left = - self._origin[0] * ImagesDict.images[self._image_name][frame].get_width() - 1
        top = - self._origin[1] * ImagesDict.images[self._image_name][frame].get_height()  - 1 
        right = (1 - self._origin[0]) * ImagesDict.images[self._image_name][frame].get_width() 
        bottom = (1 - self._origin[1]) * ImagesDict.images[self._image_name][frame].get_height() 
        return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)
    
    # def assign_mouse_hover (self, function)->Self:
    #     self.on_hover.append(function)
    #     return self
    # def assign_mouse_down (self, function)->Self:
    #     self.on_mouse_down.append(function)
    #     return self
    # def assign_mouse_drag (self, function)->Self:
    #     self.on_mouse_drag.append(function)
    #     return self
    # def assign_mouse_up (self, function)->Self:
    #     self.on_mouse_up.append(function)
    #     return self
    # def assign_delete (self, function)->Self:
    #     self.on_delete.append(function)
    #     return self
    # def assign_key_press (self, function)->Self:
    #     self.on_key_press.append(function)
    #     return self
    def assign_button (self, buttonname:str, function)->Self:
        self.on_button.append((buttonname, function))
        return self

    def set_deleted (self, deleted:bool=True) -> Self:
        self.deleted = deleted
        return self