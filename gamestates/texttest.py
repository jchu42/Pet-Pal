from gamestate import GameState
from gameobject import GameObject
from gameobjects.strinput import StrInput
import gamestates.mainmenu as mm

class TextTest(GameState):
    """This is the text test screen state."""
    def __init__(self)->None:
        GameState.__init__(self)

        self._bg_color((0, 0, 0, 255))
        self._add_game_object(GameObject ()).set_image_text("1234567890", (255, 255, 255, 255)).set_pos((30, 6))
        self._add_game_object(GameObject ()).set_image_text("!@#$%^&*()", (255, 255, 0, 255)).set_pos((30, 12))
        self._add_game_object(GameObject ()).set_image_text("-_=+[]{}\\|", (255, 0, 0, 255)).set_pos((30, 18))
        self._add_game_object(GameObject ()).set_image_text(",<.>/?;:'" + '"', (0, 0, 255, 255)).set_pos((30, 24))
        self._add_game_object(GameObject ()).set_image_text("qwertyuiop", (0, 255, 255, 255)).set_pos((30, 30))
        self._add_game_object(GameObject ()).set_image_text("asdfghjk l", (0, 255, 0, 255)).set_pos((30, 36))
        self._add_game_object(GameObject ()).set_image_text("zxcv b n m", (255, 255, 0, 122)).set_pos((30, 42))
        self._add_game_object(StrInput ()).set_pos ((1, 48)).set_color((255, 0, 255, 122))

        back_button = GameObject ().set_image_text("return", (255, 0, 0, 255)).set_pos((30, 69))
        back_button.on_mouse_up.append(lambda: self._set_state(mm.MainMenu()))
        back_button.assign_button("return", lambda:self._set_state(mm.MainMenu()))
        self._add_game_object(back_button)