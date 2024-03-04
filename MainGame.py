
# TODO:
# - database (store username/password, statuses, last time)
# - stats; stats decreasing over time
# - eating
# - cleaning up poop animation
# - hunger/health levels; display status
# - pet movements / states depending on stat values
# - login back button when entering password to edit the username


# cool instruments:
# 10, 32/34, 38, 45, 55, 81, 96, 120

# - collision events?

import sys
import pygame
import pygame.midi
from gamemanager import GameManager
from imagesdict import ImagesDict
from gamestates.room import Room
from gamestates.texttest import TextTest
from gamestates.login import Login
from gamestates.roomselector import RoomSelector
from gamestates.petselector import PetSelector
from gamestates.audiotest import AudioTest
from gamestates.mainmenu import MainMenu
from gameobject import GameObject

# configure screen
SCALE = 4
PIXELS = (60, 70)

def main() -> int:
    # pygame setup
    pygame.init() # https://stackoverflow.com/questions/50569453/why-does-it-say-that-module-pygame-has-no-init-member
    pygame.midi.init()
    GameObject.midi_out = pygame.midi.Output(pygame.midi.get_default_output_id()) # ???

    # audio = pygame.mixer.Sound("audiotest2.mp3")
    # audio.set_volume(0.2)
    #audio.play()


    # startup screen manager
    gm = GameManager(SCALE, PIXELS)
    ImagesDict(gm.drawing_surface) # static function call
    gm.add_state(Login())
    gm.add_state(TextTest())
    gm.add_state(RoomSelector())
    gm.add_state(PetSelector())
    gm.add_state(Room())
    gm.add_state(AudioTest())
    gm.add_state(MainMenu())

    gm.run("mainmenu") # login screen

if __name__ == '__main__':
    sys.exit(main())