"""Contains the Login class"""
from gamestate import GameState
from gameobject import GameObject
from gameobjects.strinput import StrInput
import gamestates.mainmenu as mm
import gamestates.room as rm
import gamestates.petselector as ps
import gamestates.error as err
import gameDatabase as db

class Login(GameState):
    """This is the login screen state."""
    def __init__(self, isRegisterScreen, username="")->None:
        """Initialize the login screen to the username entry"""
        GameState.__init__(self)
        self.isRegisterScreen = isRegisterScreen

        self._bg_color ((0, 0, 0, 255))

        self.enter_user = GameObject ().set_pos((2, 10))
        self.enter_user.set_image_text("Enter Username", (255, 0, 0, 255)).set_origin((0, 1))
        self.username = StrInput ().set_pos ((4, 16)).set_color((0, 255, 255, 0))
        self.username.set_text(username)
        self._add_game_object(self.enter_user)
        self._add_game_object(self.username)

        self.back_button = GameObject ().set_image_text("BACK", (255, 0, 0, 255))
        self.back_button.set_pos((1, 69)).set_origin((0, 1))
        self.back_button.on_mouse_up.append(lambda: self._set_state(mm.MainMenu()))
        self.back_button.assign_button("escape", lambda:self._set_state(mm.MainMenu()))
        self._add_game_object(self.back_button)

        self.next_button = GameObject ().set_pos((30, 69))
        self.next_button.set_image_text("NEXT", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(self.__change_to_password)
        self.next_button.assign_button("return", self.__change_to_password)
        self.next_button.assign_button("tab", self.__change_to_password)
        self._add_game_object(self.next_button)

        self.enter_pass = None
        self.password = None

    def __change_to_password (self)->None:
        """Change from username entry to password entry"""
        self.username.set_deleted()
        self.next_button.set_deleted()
        self.back_button.set_deleted()

        self.enter_user.set_image_text("Enter Username", (122, 0, 0, 255)).set_origin((0, 1))
        user_text = self._add_game_object(GameObject ()).set_pos((4, 16)).set_origin((0, 1))
        user_text.set_image_text(self.username.get_text(), (0, 122, 122, 255))

        back_button = GameObject ().set_image_text("BACK", (255, 0, 0, 255))
        back_button.set_pos((1, 69)).set_origin((0, 1))
        back_button.on_mouse_up.append(lambda: self._set_state(Login(self.username.get_text())))
        back_button.assign_button("escape", lambda:self._set_state(Login(self.username.get_text())))
        self._add_game_object(back_button)

        self.enter_pass = self._add_game_object(GameObject ()).set_pos((2, 28)).set_origin((0, 1))
        self.enter_pass.set_image_text("Enter Password", (255, 0, 0, 255))
        self.password = StrInput ().set_pos ((4, 34)).set_color((0, 255, 255, 0)).set_censored(True)
        self._add_game_object(self.password)

        self.next_button = GameObject ().set_pos((30, 69))
        self.next_button.set_image_text("NEXT", (255, 0, 0, 255))
        self.next_button.on_mouse_up.append(self.__verify_credentials)
        self.next_button.assign_button("return", self.__verify_credentials)
        self._add_game_object(self.next_button)

    def __verify_credentials(self)->None:
        if self.isRegisterScreen:
            if db.get_pet (self.username.get_text()) is None:
                db.add_user(self.username.get_text(), self.password.get_text())
                self._set_state(ps.PetSelector(self.username.get_text()))
            else:
                self._set_state(err.Error("Error", ["Username already", "exists!"], Login(True)))
        else:
            if db.verify_user(self.username.get_text(), self.password.get_text()):
                # if verified, proceed
                pet_type, pet_room, pet_happy, poops = db.get_pet(self.username.get_text())
                # go to pet selector if current pet is none
                if pet_type == "":
                    self._set_state(ps.PetSelector(self.username.get_text()))
                else:
                    self._set_state(rm.Room(self.username.get_text()))
            else:
                self._set_state(err.Error("Error", ["Wrong username", "/password!"], Login(False, self.username.get_text())))
