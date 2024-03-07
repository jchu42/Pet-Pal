"""Contains the RoomSelector class"""
import time
from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.room as rm
import gameDatabase as db

class RoomSelector(GameState):
    """This is the room selection screen state"""
    def __init__(self, username, petname)->None:
        """Initialize the room selection screen, which uses a Selector for the user to peruse and select a room"""
        GameState.__init__(self)
        self.username = username
        self.petname = petname

        self._bg_color ((0, 0, 0, 255))

        self.room_selector = Selector(options=["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        self.room_selector.lessthan.set_pos((5, 53)).set_origin((0.5, 1))
        self.room_selector.lessthan.on_button.append(("w", self.room_selector.decrement))
        self.room_selector.morethan.set_pos((55, 53)).set_origin((0.5, 1))
        self.room_selector.morethan.on_button.append(("s", self.room_selector.increment))
        self._add_game_object(self.room_selector)

        border_names = []
        for i in range(20):
            border_names.append("border" + str(i))
        border_names.append("")
        self.border_selector = Selector(options=border_names, color=(255, 255, 255, 255))
        self.border_selector.lessthan.set_pos((5, 59)).set_origin((0.5, 1))
        self.border_selector.lessthan.on_button.append(("a", self.border_selector.decrement))
        self.border_selector.morethan.set_pos((55, 59)).set_origin((0.5, 1))
        self.border_selector.morethan.on_button.append(("d", self.border_selector.increment))
        self._add_game_object(self.border_selector)

        next_button = GameObject (imagetext=("NEXT", (255, 0, 0, 255)),
                                  pos=(30, 59),
                                  on_mouse_up=[self.__change_state],
                                  on_button=[("return", self.__change_state),
                                             ("space", self.__change_state)])
        self._add_game_object(next_button)

    def __change_state(self):
        """Go to the next GameState"""
        db.set_pet(self.username,
                   pet_type=self.petname,
                   room_type=self.room_selector.get_option(),
                   border_type=self.border_selector.get_option(),
                   last_updated=time.time())
        self._set_state(rm.Room(username=self.username))
