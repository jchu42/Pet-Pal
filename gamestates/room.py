from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
import gamestates.texttest as tt

class Room(GameState):
    def __init__(self, roomname:str, petname:str)->None:
        GameState.__init__(self)

        self.main_ui(roomname)

        main_pet = MainPet (petname).set_pos((30, 30))
        self.add_game_object(main_pet)
        
        text_test = GameObject ().set_pos((30, 69)).set_image_text("frefGvVB", (255, 0, 0, 255), True)
        text_test.on_mouse_up.append(lambda: self.set_state(tt.TextTest()))
        self.add_game_object(text_test)
