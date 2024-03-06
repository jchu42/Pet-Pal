"""Contains the Room class"""
from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
import gamestates.texttest as tt
import gameDatabase as db

class Room(GameState):
    """This is the main room screen state."""
    def __init__(self, username:str)->None:
        """Initialize the room with the pet
        
        Parameters
        ----------
        roomname : str
            The background image to use
        petname : str
            The name of the pet to use
        """
        GameState.__init__(self)

        pet_type, room_type, border_type, pet_happy, poops = db.get_pet(username)

        self._main_ui(room_type, border_type)
        
        main_pet = MainPet (pet_type, pet_happy, poops).set_pos((30, 30))
        self._add_game_object(main_pet)

        text_test = GameObject ().set_pos((30, 59)).set_image_text("TEXT TEST", (255, 0, 0, 255))
        text_test.on_mouse_up.append(lambda: self._set_state(tt.TextTest()))
        self._add_game_object(text_test)
