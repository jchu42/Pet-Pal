"""Contains the MainMenu class"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.texttest as tt
import gamestates.audiotest as at
import pygame

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

        login_button = GameObject ().set_image_text("LOGIN", (255, 0, 0, 255)).set_pos((30, 23)).set_origin((0.5, 0.5))
        login_button.on_mouse_up.append(lambda: self._set_state(lg.Login(False)))
        login_button.on_button.append(("l", lambda:self._set_state(lg.Login(False))))
        self._add_game_object(login_button)

        register_button = GameObject ().set_image_text("NEW", (255, 0, 0, 255)).set_pos((30, 37)).set_origin((0.5, 0.5))
        register_button.on_mouse_up.append(lambda: self._set_state(lg.Login(True)))
        register_button.on_button.append(("n", lambda:self._set_state(lg.Login(True))))
        self._add_game_object(register_button)

        text_test_button = self._add_game_object(GameObject ())
        text_test_button.set_image_text("T", (255, 0, 0, 255)).set_pos((1, 1)).set_origin((0, 0))
        text_test_button.on_mouse_up.append(lambda: self._set_state(tt.TextTest()))
        text_test_button.on_button.append(("t", lambda:self._set_state(tt.TextTest)))

        audio_test_button = self._add_game_object(GameObject ())
        audio_test_button.set_image_text("A", (255, 0, 0, 255)).set_pos((1, 7)).set_origin((0, 0))
        audio_test_button.on_mouse_up.append(lambda: self._set_state(at.AudioTest()))
        audio_test_button.on_button.append(("a", lambda:self._set_state(at.AudioTest())))

        quit_button = self._add_game_object(GameObject())
        quit_button.set_image_text("QUIT", (255, 0, 0, 255)).set_pos((30, 59))
        quit_button.on_mouse_up.append(lambda: self._set_state(None))
        quit_button.on_button.append(("q", lambda:self._set_state(None)))
        quit_button.on_button.append(("escape", lambda:self._set_state(None)))

        self.music_button = self._add_game_object(GameObject()).set_pos((0, 60)).set_origin((0, 1))
        self.music_button.on_mouse_up = [self.set_music_button]
        self.music_button.on_button = [ (("m", self.set_music_button))]
        self.playing = music.get_busy()
        if self.playing:
            self.music_button.set_image_name("musicon")
        else:
            self.music_button.set_image_name("musicoff")
            
    
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