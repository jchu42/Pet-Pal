"""Contains the MainMenu class"""
import pygame
from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.texttest as tt
import gamestates.audiotest as at
import gameobjects.poop as pp

pygame.mixer.init()
music = pygame.mixer.music
music.load('Sakura-Girl-Lucky-Day.wav')
music.play(-1)
music.set_volume(0.1)

class MainMenu(GameState):
    """This is the main menu screen state."""
    def __init__(self)->None:
        """Loads the main menu screen with login, text test, audio test, and quit"""
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        mainbg = self._add_game_object(GameObject())
        mainbg.set_image_name("mainbg").set_pos((30, 60))

        self._add_game_object(GameObject (imagetext=("LOGIN", (255, 0, 0, 255)),
                                          pos=(30, 23),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(lg.Login(False))],
                                          on_button=[("l",lambda: self._set_state(lg.Login(False)))]))

        self._add_game_object(GameObject (imagetext=("NEW", (255, 0, 0, 255)),
                                          pos=(30, 37),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(lg.Login(True))],
                                          on_button=[("n",lambda: self._set_state(lg.Login(True)))]))

        self._add_game_object(GameObject (imagetext=("T", (255, 0, 0, 255)),
                                          pos=(1, 1),
                                          origin=(0, 0),
                                          on_mouse_up=[lambda: self._set_state(tt.TextTest())],
                                          on_button=[("t",lambda: self._set_state(tt.TextTest()))]))

        self._add_game_object(GameObject (imagetext=("A", (255, 0, 0, 255)),
                                          pos=(1, 7),
                                          origin=(0, 0),
                                          on_mouse_up=[lambda: self._set_state(at.AudioTest())],
                                          on_button=[("a",lambda: self._set_state(at.AudioTest()))]))

        self._add_game_object(GameObject(imagetext=("QUIT", (255, 0, 0, 255)),
                                         pos=(30, 59),
                                         on_mouse_up=[lambda: self._set_state(None)],
                                         on_button=[("q",lambda: self._set_state(None)),
                                                    ("escape",lambda: self._set_state(None))]))

        self.playing = music.get_busy()
        self.music_button = self._add_game_object(GameObject(pos=(0, 60),
                                                             imagename="musicon" if self.playing else "musicoff",
                                                             origin=(0, 1),
                                                             on_mouse_up=[self.set_music_button],
                                                             on_button=[("m", self.set_music_button)]))
            
    
    def set_music_button (self):
        """Toggles music and button"""
        self.playing = not self.playing
        if self.playing:
            self.music_button.set_image_name("musicon")
            music.play(-1)
        else:
            self.music_button.set_image_name("musicoff")
            music.stop()


        # rip = self._add_game_object(GameObject())
        # rip.set_image_name("rip").set_pos((30, 30))