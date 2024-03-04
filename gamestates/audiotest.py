from gamestate import GameState
from gameobject import GameObject
from gameobjects.mainpet import MainPet
from gameobjects.strinput import StrInput
from gameobjects.selector import Selector
import gamestates.mainmenu as mm

class AudioTest(GameState):
    def __init__(self)->None:
        GameState.__init__(self)

        self.bg_color ((255, 255, 255, 255))

        self.add_game_object(GameObject ()).set_image_text("Pitch").set_pos((30, 7))
        self.pitch = Selector([x*25+25 for x in range (160)], color=(255, 0, 0, 255)).set_pos((30, 14)).set_muted(True)
        self.pitch.selection = 3
        self.pitch.lessthan.on_mouse_up.append(self.buttonSound)
        self.pitch.morethan.on_mouse_up.append(self.buttonSound)
        self.add_game_object(self.pitch)
        self.add_game_object(GameObject ()).set_image_text("Instrument").set_pos((30, 24))
        self.instrument = Selector([x for x in range (128)], color=(255, 0, 0, 255)).set_pos((30, 31)).set_muted(True)
        self.instrument.lessthan.on_mouse_up.append(self.buttonSound)
        self.instrument.morethan.on_mouse_up.append(self.buttonSound)
        self.add_game_object(self.instrument)
        self.add_game_object(GameObject ()).set_image_text("Volume").set_pos((30, 41))
        self.volume = Selector([x*4 for x in range(31)], color=(255, 0, 0, 255)).set_pos((30, 47)).set_muted(True)
        self.volume.selection = 25
        self.volume.lessthan.on_mouse_up.append(self.buttonSound)
        self.volume.morethan.on_mouse_up.append(self.buttonSound)
        self.add_game_object(self.volume)

        self.play_button = GameObject().set_pos((30, 58)).set_image_text("Play", (255, 0, 255, 255))
        self.play_button.on_mouse_down.append(self.buttonSound)
        self.add_game_object(self.play_button)

        login_button = GameObject ().set_image_text("Return", (255, 0, 0, 255), True).set_pos((30, 69))
        login_button.on_mouse_up.append(lambda: self.set_state(mm.MainMenu()))
        login_button.assign_button("return", lambda:self.set_state(mm.MainMenu()))
        self.add_game_object(login_button)

    def buttonSound(self) -> None:
        self.play_button.play_sound(self.pitch.get_option(), self.instrument.get_option(), self.volume.get_option())