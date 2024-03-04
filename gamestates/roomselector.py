from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector

class RoomSelector(GameState):
    def get_name(self)->str:
        return "roomselector"
    def load_state(self, petname:str, *args, **wargs)->None:
        self.bg_color ((0, 0, 0, 255))

        selector = Selector(["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        selector.lessthan.set_pos((5, 69))
        selector.morethan.set_pos((55, 69))
        self.add_game_object(selector)

        next_button = GameObject ().set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        next_button.on_mouse_up.append(lambda: self.set_state("room", roomname=selector.get_option(), petname=petname))
        next_button.assign_button("return", lambda:self.set_state("room", roomname=selector.get_option(), petname=petname))
        self.add_game_object(next_button)