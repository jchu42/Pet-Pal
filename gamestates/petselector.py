from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.roomselector as rm

class PetSelector(GameState):
    """This is the pet selection screen state."""
    def __init__(self)->None:
        GameState.__init__(self)

        self._bg_color ((255, 255, 255, 255))

        selector = Selector(["pandaidle", "catidle"], color=(0, 0, 0, 255))
        self._add_game_object(selector)
        next_button = self._add_game_object(GameObject ()).set_image_text("Next", (255, 0, 0, 255)).set_pos((30, 69))
        next_button.on_mouse_up.append(lambda: self._set_state(rm.RoomSelector(petname=selector.get_option().removesuffix("idle"))))
        next_button.on_button.append(("return", lambda:self._set_state(rm.RoomSelector(petname=selector.get_option().removesuffix("idle")))))
       