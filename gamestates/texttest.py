from gamestate import GameState
from gameobject import GameObject
from gameobjects.strinput import StrInput
import gamestates.mainmenu as mm

class TextTest(GameState):
    """This is the text test screen state."""
    def __init__(self)->None:
        """Create the text test screen, showing every character and a textbox entry"""
        GameState.__init__(self)

        self._bg_color((0, 0, 0, 255))

        text = ["`1234567890-=",
                "~!@#$%^&*()_+",
                "qwertyuiop[]\\",
                "QWERTYUIOP{}|",
                "asdfghjkl;'",
                'ASDFGHJKL:"',
                "zxcvbnm,./",
                "ZXCVBNM<>?"]

        for y, line in enumerate(text):
            for x, char in enumerate(line):
                r = 255 - max(255/len(line)*x*2 - 255, 0)
                g = min(255/len(line)*x*2, 255)
                b = 255/len(text)*y
                self._add_game_object(GameObject(imagetext=(char, (r, g, b, 255)),
                                                 pos=(1+4*x, 6+6*y),
                                                 origin=(0, 1)))

        # self._add_game_object(GameObject ()).set_image_text((255, 255, 255, 255)).set_pos((30, 5))
        # self._add_game_object(GameObject ()).set_image_text((255, 255, 0, 255)).set_pos((30, 10))
        # self._add_game_object(GameObject ()).set_image_text( (255, 0, 0, 255)).set_pos((30, 15))
        # self._add_game_object(GameObject ()).set_image_text((0, 0, 255, 255)).set_pos((30, 20))
        # self._add_game_object(GameObject ()).set_image_text((0, 255, 255, 255)).set_pos((30, 25))
        # self._add_game_object(GameObject ()).set_image_text((0, 255, 0, 255)).set_pos((30, 30))
        # self._add_game_object(GameObject ()).set_image_text((255, 122, 0, 122)).set_pos((30, 35))
        # self._add_game_object(GameObject ()).set_image_text(, (0, 122, 255, 255)).set_pos((30, 40))
        self.input = StrInput ()
        self._add_game_object(self.input)
        self.input.set_pos ((59, 47)).set_color((255, 0, 255, 122)).set_char_limit(99999999).set_origin((1, 1))

        back_button = GameObject ().set_image_text("RETURN", (255, 0, 0, 255)).set_pos((30, 59))
        back_button.on_mouse_up.append(lambda: self._set_state(mm.MainMenu()))
        back_button.assign_button("escape", lambda:self._set_state(mm.MainMenu()))
        self._add_game_object(back_button)
    # def move_text_back (self, string:str):
    #     """Move the input to the left when it gets too long, so new characters input can still be seen
        
    #     Parameters
    #     ----------
    #     string : str
    #         The key pressed; required to hook onto key press functions
    #     """
    #     if len(self.input.text) > 14:
    #         self.input.set_pos((1 - (len(self.input.text) - 14)*4, self.input.get_pos()[1]))