"""Contains the AudioTest module"""
from gamestate import GameState
from gameobject import GameObject
import gamestates.mainmenu as mm
from gameobjects.selector import Selector

class AudioTest(GameState):
    """This is the audio test state, used to test MIDI pitch, instrument, and volume parameters"""
    def __init__(self)->None:
        """Initialize the audio test state, with 3 selectors for audio settings, and a play audio button."""
        GameState.__init__(self)

        self._bg_color ((255, 255, 255, 255))

        self._add_game_object(GameObject (imagetext=("PITCH"), pos=(30, 7)))
        self.pitch = Selector(options=[x for x in range (128)],
                              initial_selection=50,
                              muted=True,
                              color=(255, 0, 0, 255),
                              pos_all=(30, 14),
                              origin_all=(0.5, 1))
        self.pitch.lessthan.on_mouse_up.append(self.__button_sound)
        self.pitch.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.pitch)

        self._add_game_object(GameObject (imagetext=("INSTRUMENT"), pos=(30, 22)))
        self.instrument = Selector(options=[x for x in range (128)],
                                   color=(255, 0, 0, 255),
                                   pos_all=(30, 29),
                                   muted=True,
                                   origin_all=(0.5, 1))
        self.instrument.lessthan.on_mouse_up.append(self.__button_sound)
        self.instrument.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.instrument)

        self._add_game_object(GameObject (imagetext=("VOLUME"), pos=(30, 37)))
        self.volume = Selector(options=[x*4 for x in range(32)],
                               initial_selection=25,
                               color=(255, 0, 0, 255),
                               pos_all=(30, 44),
                               muted=True,
                               origin_all=(0.5, 1))
        self.volume.lessthan.on_mouse_up.append(self.__button_sound)
        self.volume.morethan.on_mouse_up.append(self.__button_sound)
        self._add_game_object(self.volume)

        self.play_button = GameObject(pos=(30, 52),
                                      imagetext=("PLAY", (255, 0, 255, 255)),
                                      on_mouse_down=[self.__button_sound])
        self._add_game_object(self.play_button)

        self._add_game_object(GameObject (imagetext=("RETURN", (255, 0, 0, 255)),
                                          pos=(30, 59),
                                          on_mouse_up=[lambda: self._set_state(mm.MainMenu())],
                                          on_button=[("escape", lambda:self._set_state(mm.MainMenu()))]))

    def __button_sound(self) -> None:
        """Play the MIDI with the currently selected options"""
        self.play_button.queue_sound(self.pitch.get_option(),
                                     self.instrument.get_option(),
                                     self.volume.get_option())
