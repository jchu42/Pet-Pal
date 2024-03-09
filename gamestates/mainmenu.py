"""Contains the MainMenu class"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.test as tt

class MainMenu(GameState):
    """This is the main menu screen state."""
    def __init__(self)->None:
        """Loads the main menu screen with login, new, quit, and test buttons"""
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        mainbg = self._add_game_object(GameObject())
        mainbg.set_image_name("mainbg").set_pos((30, 60))

        self._add_game_object(GameObject (imagetext=("LOGIN", (235, 250, 122, 255)),
                                          pos=(30, 23),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(lg.Login(False))],
                                          on_button=[("l",lambda: self._set_state(lg.Login(False)))]))

        self._add_game_object(GameObject (imagetext=("NEW", (235, 250, 122, 255)),
                                          pos=(30, 37),
                                          origin=(0.5, 0.5),
                                          on_mouse_up=[lambda: self._set_state(lg.Login(True))],
                                          on_button=[("n",lambda: self._set_state(lg.Login(True)))]))

        self._add_game_object(GameObject (imagetext=("Test", (188, 107, 242, 255)),
                                          pos=(1, 1),
                                          origin=(0, 0),
                                          on_mouse_up=[lambda: self._set_state(tt.Test())],
                                          on_button=[("t",lambda: self._set_state(tt.Test()))]))

        self._add_game_object(GameObject(imagetext=("QUIT", (0, 125, 255, 255)),
                                         pos=(30, 59),
                                         on_mouse_up=[lambda: self._set_state(None)],
                                         on_button=[("q",lambda: self._set_state(None)),
                                                    ("escape",lambda: self._set_state(None))]))
