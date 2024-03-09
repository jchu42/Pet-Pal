"""Contains the Room class"""
from gamestate import GameState
import gamestates.mainmenu as mm
import gamestates.death as dt
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gamedatabase import GameDatabase as db

class Room(GameState):
    """This is the main room screen state."""
    def __init__(self, username:str)->None:
        """Initialize the room with the pet
        
        Parameters
        ----------
        username : str
            The user's username
        """
        GameState.__init__(self)
        self.username = username
        (pet_type,
         room_type,
         border_type,
         pet_hunger,
         poops,
         last_updated) = db.get_pet(username, (db.PET_TYPE,
                                               db.ROOM_TYPE,
                                               db.BORDER_TYPE,
                                               db.PET_HUNGER,
                                               db.POOPS,
                                               db.LAST_UPDATED))

        self._main_ui(room_type, border_type)

        self.main_pet = MainPet (username, pet_type, pet_hunger, poops, last_updated, pos=(30, 30))
        self._add_game_object(self.main_pet)

        self._add_game_object(GameObject(on_button=[("escape", lambda: self._set_state(mm.MainMenu()))]))

    def _state_tick(self) -> None:
        """Check if the pet has died each frame. If dead, trigger death screen."""
        if self.main_pet.goodbye_forever:
            self._set_state(dt.Death(self.username))
