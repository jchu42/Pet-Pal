from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector

class PetSelector(GameState):
    def get_name(self)->str:
        return "petselector"
    def load_state(self, *args, **wargs)->None:
        self.bg_color ((255, 255, 255, 255))

        selector = Selector(["pandaidle", "catidle"], (0, 0, 0, 255))
        self.add_game_object(selector)
        nextButton = self.add_game_object(GameObject ()).set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        nextButton.on_mouse_up.append(lambda: self.set_state("roomselector", petname=selector.get_option().removesuffix("idle")))
        nextButton.on_button.append(("return", lambda:self.set_state("roomselector", petname=selector.get_option().removesuffix("idle"))))
       