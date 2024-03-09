"""Contains the Test class"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.mainmenu as mm
import gamestates.texttest as tt
import gamestates.audiotest as at

class Test(GameState):
    """This is the test options screen state."""
    def __init__(self)->None:
        """Loads the test screen with text and audio test buttons"""
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        self._add_game_object(GameObject (imagetext=("Text Test", (188, 107, 242, 255)),
                                          pos=(30, 25),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(tt.TextTest())],
                                          on_button=[("t",lambda: self._set_state(tt.TextTest()))]))

        self._add_game_object(GameObject (imagetext=("Audio Test", (188, 107, 242, 255)),
                                          pos=(30, 35),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(at.AudioTest())],
                                          on_button=[("a",lambda: self._set_state(at.AudioTest()))]))

        self._add_game_object(GameObject (imagetext=("Return", (188, 107, 242, 255)),
                                          pos=(30, 59),
                                          origin=(0.5, 1),
                                          on_mouse_up=[lambda: self._set_state(mm.MainMenu())],
                                          on_button=[("backspace",lambda: self._set_state(mm.MainMenu())),
                                                     ("m",lambda: self._set_state(mm.MainMenu()))]))
