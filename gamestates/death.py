"""Contains the Death class for when the pet dies"""
from gamestate import GameState
from gameobject import GameObject
from gamestates.petselector import PetSelector
from gamedatabase import GameDatabase as db

class Death(GameState):
    """This is the pet death screen state."""
    def __init__(self, username:str)->None:
        """Initialize pet death screen"""
        GameState.__init__(self)

        self._bg_color((0, 255, 0, 255))
        self._add_game_object(GameObject(imagename="rip", pos=(30, 30), origin=(0.5, 0.5)))

        self._add_game_object(GameObject(imagetext=("start over", (0, 0, 0, 255)),
                                         pos=(30, 59),
                                         origin=(0.5, 1),
                                         on_mouse_up=[lambda:self._set_state(PetSelector(username))]))

        db.set_pet(username=username, pet_type="")
