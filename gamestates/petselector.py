"""Contains the PetSelector class"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.roomselector as rs
import gamestates.login as lg
from gameobjects.selector import Selector

class PetSelector(GameState):
    """This is the pet selection screen state."""
    def __init__(self, username)->None:
        """Initializese the pet selection screen; uses a Selector for the user to select a pet."""
        GameState.__init__(self)
        self.username = username
        self._bg_color ((127, 209, 255, 255))

        self.selector = Selector(options=["pandaidle", "catidle", "pigidle"], color=(0, 0, 0, 255))
        self.selector.lessthan.on_button.append(("a", self.selector.decrement))
        self.selector.morethan.on_button.append(("d", self.selector.increment))
        self._add_game_object(self.selector)

        self._add_game_object(GameObject (pos=(30, 59),
                                          imagetext=("NEXT", (255, 0, 0, 255)),
                                          on_mouse_up=[self.__change_state],
                                          on_button=[("return", self.__change_state),
                                                     ("space", self.__change_state)]))
        #next_button.set_image_text("NEXT", (255, 0, 0, 255))
        #next_button.on_mouse_up.append(self.__change_state)
        # next_button.on_button.append(("return", self.__change_state))
        # next_button.on_button.append(("space", self.__change_state))

        self._add_game_object(GameObject (imagetext=("BACK", (255, 0, 0, 255)),
                                          pos=(1, 59),
                                          origin=(0, 1),
                                          on_mouse_up=[self.__change_back],
                                          on_button=[("escape", self.__change_back)]))

    def __change_state(self):
        """Go to the next GameState"""
        self._set_state(rs.RoomSelector(username=self.username, 
                                        petname=self.selector.get_option().removesuffix("idle")))
    def __change_back(self):
        """Go to login screen"""
        self._set_state(lg.Login(is_register_screen=False, username=self.username))