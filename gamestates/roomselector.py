from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.room as rm

class RoomSelector(GameState):
    def __init__(self, petname:str)->None:
        GameState.__init__(self)
        
        self.bg_color ((0, 0, 0, 255))

        selector = Selector(["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        selector.lessthan.set_pos((5, 69))
        selector.morethan.set_pos((55, 69))
        self.add_game_object(selector)

        next_button = GameObject ().set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        next_button.on_mouse_up.append(lambda: self.set_state(rm.Room(roomname=selector.get_option(), petname=petname)))
        next_button.assign_button("return", lambda:self.set_state(rm.Room(roomname=selector.get_option(), petname=petname)))
        self.add_game_object(next_button)