from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class TextTest(GameState):
    def get_name(self)->str:
        return "texttest"
    def load_state(self, *args, **wargs)->None:
        self.bg_color((0, 0, 0, 255))
        self.add_game_object(GameObject ()).set_image_text("1234567890", (255, 255, 255, 255), True).set_pos((30, 6))
        self.add_game_object(GameObject ()).set_image_text("!@#$%^&*()", (255, 255, 0, 255), True).set_pos((30, 12))
        self.add_game_object(GameObject ()).set_image_text("-_=+[]{}\\|", (255, 0, 0, 255), True).set_pos((30, 18))
        self.add_game_object(GameObject ()).set_image_text(",<.>/?;:'" + '"', (0, 0, 255, 255), True).set_pos((30, 24))
        self.add_game_object(GameObject ()).set_image_text("qwertyuiop", (0, 255, 255, 255), True).set_pos((30, 30))
        self.add_game_object(GameObject ()).set_image_text("asdfghjk l", (0, 255, 0, 255), True).set_pos((30, 36))
        self.add_game_object(GameObject ()).set_image_text("zxcv b n m", (255, 255, 0, 122), True).set_pos((30, 42))
        self.add_game_object(StrInput ()).set_pos ((1, 48)).set_color((255, 0, 255, 122))

        back_button = GameObject ().set_image_text("return", (255, 0, 0, 255), True).set_pos((30, 69))
        back_button.on_mouse_up.append(lambda: self.set_state("mainmenu"))
        back_button.assign_button("return", lambda:self.set_state("mainmenu"))
        self.add_game_object(back_button)