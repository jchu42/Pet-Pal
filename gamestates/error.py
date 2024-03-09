"""Contains the Error class"""
from gamestate import GameState
from gameobject import GameObject

class Error(GameState):
    """This is the error screen state."""
    def __init__(self, error:str, description:list[str], next_state:GameState)->None:
        """Create the error screen based on the parameters
        
        Parameters
        ----------
        error : str
            The title to show, typically 'Error'.
        description : list[str]
            The list of lines of strings to show. 
        next_state : GameState
            The state to go to when the user exits the error screen.
        """
        GameState.__init__(self)
        self._bg_color ((0, 0, 0, 255))

        self.next_state = next_state
        self.error = GameObject().set_pos((30, 8)).set_image_text(error, (255, 0, 0, 255))
        self._add_game_object(self.error)

        for index, desc_line in enumerate(description):
            self._add_game_object(GameObject(pos=(1, 16 + index*6),
                                             imagetext=(desc_line, (255, 255, 255, 255)),
                                             origin=(0, 1)))

        self.next_button = GameObject ().set_pos((30, 59))
        self.next_button.set_image_text("BACK", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(self.__go_back)
        self.next_button.assign_button("return", self.__go_back)
        self.next_button.assign_button("escape", self.__go_back)
        self.next_button.assign_button("space", self.__go_back)
        self._add_game_object(self.next_button)

    def __go_back (self)->None:
        """Go to the next state"""
        self._set_state(self.next_state)
