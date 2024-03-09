"""Contains the Login class"""
import psycopg2
from gamestate import GameState
from gameobject import GameObject
from gameobjects.strinput import StrInput
import gamestates.mainmenu as mm
import gamestates.room as rm
import gamestates.petselector as ps
import gamestates.error as err
from gamedatabase import GameDatabase as db

class Login(GameState):
    """This is the login screen state."""
    def __init__(self, is_register_screen:bool, username:str="")->None:
        """Initialize the login screen to the username entry
        
        Parameters
        ----------
        is_register_screen : bool
            True if this should be a register screen, False if this should be a login screen
        username : str, default=""
            The previously entered username, if any.
        """
        GameState.__init__(self)
        self.is_register_screen = is_register_screen

        self._bg_color ((0, 125, 255, 255))

        title = GameObject(pos=(30, 10))
        if is_register_screen:
            title.set_image_text("Register", (255, 255, 255, 255))
        else:
            title.set_image_text("Login", (255, 255, 255, 255))
        self._add_game_object(title)

        self.enter_user = GameObject (imagetext=("Enter Username", (255, 0, 0, 255)),
                                      pos=(2,22),
                                      origin=(0, 1))
        self._add_game_object(self.enter_user)
        self.username = StrInput (pos=(4, 28),
                                  color=(0, 255, 255, 0),
                                  initial_text=username)
        self._add_game_object(self.username)

        self.back_button = GameObject (imagetext=("BACK", (255, 0, 0, 255)),
                                       pos=(1, 59),
                                       origin=(0, 1),
                                       on_mouse_up=[lambda: self._set_state(mm.MainMenu())],
                                       on_button=[("escape", lambda:self._set_state(mm.MainMenu()))])
        self._add_game_object(self.back_button)

        self.next_button = GameObject (imagetext=("NEXT", (255, 0, 0, 255)),
                                       pos=(30, 59),
                                       on_mouse_up=[self.__change_to_password],
                                       on_button=[("return", self.__change_to_password),
                                                  ("tab", self.__change_to_password)])
        self._add_game_object(self.next_button)

        self.enter_pass = None
        self.password = None

    def __change_to_password (self)->None:
        """Change from username entry to password entry"""
        self.username.set_deleted()
        self.next_button.set_deleted()
        self.back_button.set_deleted()

        self.enter_user.set_image_text("Enter Username", (122, 0, 0, 255))
        self._add_game_object(GameObject (imagetext=(self.username.get_text(), (0, 122, 122, 255)),
                                          pos=(4, 28),
                                          origin=(0, 1)))

        back_button = GameObject (imagetext=("BACK", (255, 0, 0, 255)),
                                  pos=(1, 59),
                                  origin=(0, 1),
                                  on_mouse_up=[lambda: self._set_state(Login(self.username.get_text()))],
                                  on_button=[("escape", lambda:self._set_state(Login(self.username.get_text())))])
        self._add_game_object(back_button)

        self.enter_pass = self._add_game_object(GameObject (imagetext=("Enter Password", (255, 0, 0, 255)),
                                                            pos=(2, 40),
                                                            origin=(0, 1)))
        self.password = StrInput (pos=(4, 46),
                                  color=(0, 255, 255, 0),
                                  censored=True)
        self._add_game_object(self.password)

        self.next_button = GameObject (imagetext=("NEXT", (255, 0, 0, 255)),
                                       pos=(30, 59),
                                       on_mouse_up=[self.__verify_credentials],
                                       on_button=[("return", self.__verify_credentials)])
        self._add_game_object(self.next_button)

    def __verify_credentials(self)->None:
        """Call database to verify credentials, giving user an error if necessary"""
        if self.is_register_screen:
            if (self.username.get_text() == "" or self.password.get_text() == ""):
                self._set_state(err.Error("Error", ["Please enter a", "username and", "password"], Login(True)))
            try:
                db.add_user(self.username.get_text(), self.password.get_text())
                self._set_state(ps.PetSelector(self.username.get_text()))
            except psycopg2.DatabaseError:
                self._set_state(err.Error("Error", ["Username", "already exists!"], Login(True)))
        else:
            if (self.username.get_text() == "" or self.password.get_text() == ""):
                self._set_state(err.Error("Error", ["Please enter a", "username and", "password"], Login(False)))
            if db.verify_user(self.username.get_text(), self.password.get_text()):
                # if verified, proceed
                (pet_type,) = db.get_pet(self.username.get_text(), db.PET_TYPE)
                # go to pet selector if current pet is none
                if pet_type == "" or pet_type is None:
                    self._set_state(ps.PetSelector(self.username.get_text()))
                else:
                    self._set_state(rm.Room(self.username.get_text()))
            else:
                self._set_state(err.Error("Error", ["Wrong", "username", "/password!"], Login(False, self.username.get_text())))
