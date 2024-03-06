"""Contains the Login class"""
from gamestate import GameState
from gameobject import GameObject

class Error(GameState):
    """This is the login screen state."""
    def __init__(self, error:str, description:list[str], nextState:GameState)->None:
        """Initialize the login screen to the username entry"""
        GameState.__init__(self)
        self._bg_color ((0, 0, 0, 255))

        self.nextState = nextState
        self.error = GameObject().set_pos((30, 8)).set_image_text(error, (255, 0, 0, 255))
        self._add_game_object(self.error)

        for index, descLine in enumerate(description):
            self._add_game_object(GameObject()).set_pos((1, 16 + index*6)).set_image_text(descLine, (255, 255, 255, 255)).set_origin((0, 1))
        

        self.next_button = GameObject ().set_pos((30, 63))
        self.next_button.set_image_text("BACK", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(self.__go_back)
        self.next_button.assign_button("return", self.__go_back)
        self.next_button.assign_button("escape", self.__go_back)
        self._add_game_object(self.next_button)

    def __go_back (self)->None:
        self._set_state(self.nextState)