"""Contains the RoomSelector class"""
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

        self.selector = Selector(["room", "room2", "kitchen"], color=(255, 255, 255, 255))
        self.selector.lessthan.set_pos((5, 69)).set_origin((0.5, 1))
        self.selector.morethan.set_pos((55, 69)).set_origin((0.5, 1))
        self.selector.lessthan.on_button.append(("a", self.selector.decrement))
        self.selector.morethan.on_button.append(("d", self.selector.increment))
        self._add_game_object(self.selector)

        next_button = GameObject ().set_image_text("NEXT", (255, 0, 0, 255)).set_pos((30, 69))
        next_button.on_mouse_up.append(self.__change_state)
        next_button.assign_button("return", self.__change_state)
        next_button.on_button.append(("space", self.__change_state))
        self._add_game_object(next_button)

    def __change_state(self):
        """Go to the next GameState"""
        db.set_pet(self.username, self.petname, self.selector.get_option(), 5, 0)
        self._set_state(rm.Room(username=self.username))
