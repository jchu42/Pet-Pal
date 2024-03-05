"""Contains the MainMenu class"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.texttest as tt
import gamestates.audiotest as at

class MainMenu(GameState):
    """This is the main menu screen state."""
    def __init__(self)->None:
        """Loads the main menu screen with login, text test, audio test, and quit"""
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        login_button = GameObject ().set_image_text("LOGIN", (255, 0, 0, 255)).set_pos((30, 15))
        login_button.on_mouse_up.append(lambda: self._set_state(lg.Login()))
        login_button.on_button.append(("l", lambda:self._set_state(lg.Login())))
        self._add_game_object(login_button)

        text_test_button = self._add_game_object(GameObject ())
        text_test_button.set_image_text("TEXT TEST", (255, 0, 0, 255)).set_pos((30, 30))
        text_test_button.on_mouse_up.append(lambda: self._set_state(tt.TextTest()))
        text_test_button.on_button.append(("t", lambda:self._set_state(tt.TextTest)))

        audio_test_button = self._add_game_object(GameObject ())
        audio_test_button.set_image_text("AUDIO TEST", (255, 0, 0, 255)).set_pos((30, 45))
        audio_test_button.on_mouse_up.append(lambda: self._set_state(at.AudioTest()))
        audio_test_button.on_button.append(("a", lambda:self._set_state(at.AudioTest())))

        quit_button = self._add_game_object(GameObject())
        quit_button.set_image_text("QUIT", (255, 0, 0, 255)).set_pos((30, 60))
        quit_button.on_mouse_up.append(lambda: self._set_state(None))
        quit_button.on_button.append(("q", lambda:self._set_state(None)))
        quit_button.on_button.append(("escape", lambda:self._set_state(None)))
