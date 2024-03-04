from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput

class Login(GameState):
    def get_name(self)->str:
        return "login"
    def load_state(self, *args, **wargs)->None:
        self.bg_color ((0, 0, 0, 255))

        self.enter_user = GameObject ().set_image_text("Enter Username", (255, 0, 0, 255), centered=False).set_pos((2, 10))
        self.username = StrInput ().set_pos ((4, 16)).set_color((0, 255, 255, 0))
        self.add_game_object(self.enter_user)
        self.add_game_object(self.username)

        self.next_button = GameObject ().set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        self.next_button.on_mouse_up.append(self.changeToPassword)
        self.next_button.assign_button("return", self.changeToPassword)
        self.add_game_object(self.next_button)

    def changeToPassword (self)->None:
        self.enter_user.set_image_text("Enter Username", (122, 0, 0, 255), centered=False)
        self.add_game_object(GameObject ()).set_image_text(self.username.get_text(), (0, 122, 122, 255), centered=False).set_pos((4, 16))
        self.username.set_deleted()
        self.next_button.set_deleted()

        self.add_game_object(GameObject ()).set_image_text("Enter Password", (255, 0, 0, 255), centered=False).set_pos((2, 28))        
        self.password = StrInput ().set_pos ((4, 34)).set_color((0, 255, 255, 0)).set_censored(True)
        self.add_game_object(self.password)

        self.next_button = GameObject ().set_image_text("Next", (255, 0, 0, 255), True).set_pos((30, 69))
        self.next_button.on_mouse_up.append(lambda: self.set_state("petselector"))
        self.next_button.assign_button("return", lambda:self.set_state("petselector"))
        self.add_game_object(self.next_button)
