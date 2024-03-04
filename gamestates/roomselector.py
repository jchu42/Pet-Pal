from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.room as rm

class RoomSelector(GameState):
    """This is the room selection screen state"""
    def __init__(self, petname:str)->None:
        GameState.__init__(self)
        self.petname = petname

        self._bg_color ((0, 0, 0, 255))

        self.selector = Selector(["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        self.selector.lessthan.set_pos((5, 69)).set_origin((0.5, 1))
        self.selector.morethan.set_pos((55, 69)).set_origin((0.5, 1))
        self._add_game_object(self.selector)

        next_button = GameObject ().set_image_text("Next", (255, 0, 0, 255)).set_pos((30, 69))
        next_button.on_mouse_up.append(self.__change_state)
        next_button.assign_button("return", self.__change_state)
        self._add_game_object(next_button)

    def __change_state(self):
        self._set_state(rm.Room(roomname=self.selector.get_option(), petname=self.petname))
