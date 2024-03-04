from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.texttest as tt
import gamestates.audiotest as at

class MainMenu(GameState):
    """This is the main menu screen state."""
    def __init__(self)->None:
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        login_button = GameObject ().set_image_text("Login", (255, 0, 0, 255)).set_pos((30, 20))
        login_button.on_mouse_up.append(lambda: self._set_state(lg.Login()))
        login_button.on_button.append(("return", lambda:self._set_state(lg.Login())))
        self._add_game_object(login_button)

        text_test_button = self._add_game_object(GameObject ())
        text_test_button.set_image_text("Text Test", (255, 0, 0, 255)).set_pos((30, 35))
        text_test_button.on_mouse_up.append(lambda: self._set_state(tt.TextTest()))
        text_test_button.on_button.append(("return", lambda:self._set_state(tt.TextTest)))

        audio_test_button = self._add_game_object(GameObject ())
        audio_test_button.set_image_text("Audio Test", (255, 0, 0, 255)).set_pos((30, 50))
        audio_test_button.on_mouse_up.append(lambda: self._set_state(at.AudioTest()))
        audio_test_button.on_button.append(("return", lambda:self._set_state(at.AudioTest)))
