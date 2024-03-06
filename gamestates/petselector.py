"""Contains the PetSelector class"""
from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.roomselector as rm

class PetSelector(GameState):
    """This is the pet selection screen state."""
    def __init__(self, username)->None:
        """Initializese the pet selection screen, which uses a Selector for the user to select a pet"""
        GameState.__init__(self)
        self.username = username
        self._bg_color ((255, 255, 255, 255))

        self.selector = Selector(["pandaidle", "catidle"], color=(0, 0, 0, 255))
        self._add_game_object(self.selector)
        self.selector.lessthan.on_button.append(("a", self.selector.decrement))
        self.selector.morethan.on_button.append(("d", self.selector.increment))

        next_button = self._add_game_object(GameObject ()).set_pos((30, 59))
        next_button.set_image_text("NEXT", (255, 0, 0, 255))
        next_button.on_mouse_up.append(self.__change_state)
        next_button.on_button.append(("return", self.__change_state))
        next_button.on_button.append(("space", self.__change_state))

    def __change_state(self):
        """Go to the next GameState"""
        
        self.selector.queue_sound(63) # play a sound when going to next state
        self._set_state(rm.RoomSelector(username=self.username, petname=self.selector.get_option().removesuffix("idle")))
