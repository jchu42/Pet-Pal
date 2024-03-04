from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector
import gamestates.roomselector as rm

class PetSelector(GameState):
    def __init__(self)->None:
        GameState.__init__(self)

        self.bg_color ((255, 255, 255, 255))

        selector = Selector(["pandaidle", "catidle"], (0, 0, 0, 255))
        self.add_game_object(selector)
        nextButton = self.add_game_object(GameObject ()).set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        nextButton.on_mouse_up.append(lambda: self.set_state(rm.RoomSelector(petname=selector.get_option().removesuffix("idle"))))
        nextButton.on_button.append(("return", lambda:self.set_state(rm.RoomSelector(petname=selector.get_option().removesuffix("idle")))))
       