from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Room(GameState):
    def get_name(self)->str:
        return "room"

    def load_state(self, roomname:str, petname:str, *args, **wargs)->None:
        self.main_ui(roomname)

        main_pet = MainPet (petname).set_pos((30, 30))
        self.add_game_object(main_pet)
        
        text_test = GameObject ().set_pos((30, 69)).set_image_text("frefGvVB", (255, 0, 0, 255), True)
        text_test.on_mouse_up.append(lambda: self.set_state("texttest"))
        self.add_game_object(text_test)
