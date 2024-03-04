from gamestate import GameState
from gameobject import GameObject
import gamestates.login as lg
import gamestates.texttest as tt
import gamestates.audiotest as at

class MainMenu(GameState):
    def __init__(self)->None:
        GameState.__init__(self)

        self.bg_color ((0, 0, 0, 255))
        
        login_button = GameObject ().set_image_text("Login", (255, 0, 0, 255), True).set_pos((30, 20))
        login_button.on_mouse_up.append(lambda: self.set_state(lg.Login()))
        login_button.on_button.append(("return", lambda:self.set_state(lg.Login())))
        self.add_game_object(login_button)

        text_test_button = self.add_game_object(GameObject ()).set_image_text("Text Test", (255, 0, 0, 255), True).set_pos((30, 35))
        text_test_button.on_mouse_up.append(lambda: self.set_state(tt.TextTest()))
        text_test_button.on_button.append(("return", lambda:self.set_state(tt.TextTest)))

        audio_test_button = self.add_game_object(GameObject ()).set_image_text("Audio Test", (255, 0, 0, 255), True).set_pos((30, 50))
        audio_test_button.on_mouse_up.append(lambda: self.set_state(at.AudioTest()))
        audio_test_button.on_button.append(("return", lambda:self.set_state(at.AudioTest)))

    def change_to_password (self)->None:
        # todo - combine username and password states; add a back button to go from password back to username
        pass