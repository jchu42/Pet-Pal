from gamestate import GameState
from gameobject import GameObject
from gameobjects.strinput import StrInput
import gamestates.mainmenu as mm
import gamestates.petselector as ps

class Login(GameState):
    """This is the login screen state."""
    def __init__(self, username="")->None:
        GameState.__init__(self)

        self._bg_color ((0, 0, 0, 255))

        self.enter_user = GameObject ().set_pos((2, 10))
        self.enter_user.set_image_text("Enter Username", (255, 0, 0, 255)).set_origin((0, 1))
        self.username = StrInput ().set_pos ((4, 16)).set_color((0, 255, 255, 0))
        self.username.set_text(username)
        self._add_game_object(self.enter_user)
        self._add_game_object(self.username)

        self.back_button = GameObject ().set_image_text("Back", (255, 0, 0, 255))
        self.back_button.set_pos((1, 69)).set_origin((0, 1))
        self.back_button.on_mouse_up.append(lambda: self._set_state(mm.MainMenu()))
        self._add_game_object(self.back_button)

        self.next_button = GameObject ().set_pos((30, 69))
        self.next_button.set_image_text("Next", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(self.__change_to_password)
        self.next_button.assign_button("return", self.__change_to_password)
        self._add_game_object(self.next_button)

        self.enter_pass = None
        self.password = None

    def __change_to_password (self)->None:
        self.username.set_deleted()
        self.next_button.set_deleted()
        self.back_button.set_deleted()

        self.enter_user.set_image_text("Enter Username", (122, 0, 0, 255)).set_origin((0, 1))
        user_text = self._add_game_object(GameObject ()).set_pos((4, 16)).set_origin((0, 1))
        user_text.set_image_text(self.username.get_text(), (0, 122, 122, 255))

        back_button = GameObject ().set_image_text("Back", (255, 0, 0, 255))
        back_button.set_pos((1, 69)).set_origin((0, 1))
        back_button.on_mouse_up.append(lambda: self._set_state(Login(self.username.get_text())))
        self._add_game_object(back_button)

        self.enter_pass = self._add_game_object(GameObject ()).set_pos((2, 28)).set_origin((0, 1))
        self.enter_pass.set_image_text("Enter Password", (255, 0, 0, 255))
        self.password = StrInput ().set_pos ((4, 34)).set_color((0, 255, 255, 0)).set_censored(True)
        self._add_game_object(self.password)

        self.next_button = GameObject ().set_pos((30, 69))
        self.next_button.set_image_text("Next", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(lambda: self._set_state(ps.PetSelector()))
        self.next_button.assign_button("return", lambda:self._set_state(ps.PetSelector()))
        self._add_game_object(self.next_button)
