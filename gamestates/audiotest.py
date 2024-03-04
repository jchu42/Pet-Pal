from gamestate import GameState
from gameobject import GameObject
from gameobjects.selector import Selector
import gamestates.mainmenu as mm

class AudioTest(GameState):
    """This is the audio test state, used to test MIDI pitch, instrument, and volume parameters"""
    def __init__(self)->None:
        GameState.__init__(self)

        self._bg_color ((255, 255, 255, 255))

        self._add_game_object(GameObject ()).set_image_text("Pitch").set_pos((30, 7))
        self.pitch = Selector([x for x in range (128)], 50, color=(255, 0, 0, 255))
        self.pitch.set_pos((30, 12)).set_muted(True)
        self.pitch.lessthan.on_mouse_up.append(self.__button_sound)
        self.pitch.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.pitch)
        self._add_game_object(GameObject ()).set_image_text("Instrument").set_pos((30, 24))
        self.instrument = Selector([x for x in range (128)], color=(255, 0, 0, 255))
        self.instrument.set_pos((30, 29)).set_muted(True)
        self.instrument.lessthan.on_mouse_up.append(self.__button_sound)
        self.instrument.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.instrument)
        self._add_game_object(GameObject ()).set_image_text("Volume").set_pos((30, 41))
        self.volume = Selector([x*4 for x in range(32)], 25, color=(255, 0, 0, 255))
        self.volume.set_pos((30, 45)).set_muted(True)
        self.volume.lessthan.on_mouse_up.append(self.__button_sound)
        self.volume.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.volume)

        self.play_button = GameObject().set_pos((30, 58)).set_image_text("Play", (255, 0, 255, 255))
        self.play_button.on_mouse_down.append(self.__button_sound)
        self._add_game_object(self.play_button)

        login_button = GameObject ().set_image_text("Return", (255, 0, 0, 255))
        login_button.set_pos((30, 69))
        login_button.on_mouse_up.append(lambda: self._set_state(mm.MainMenu()))
        login_button.assign_button("return", lambda:self._set_state(mm.MainMenu()))
        self._add_game_object(login_button)

    def __button_sound(self) -> None:
        self.play_button._play_sound(self.pitch.get_option(), self.instrument.get_option(), self.volume.get_option())
