
# cool instruments:
# 10, 32/34, 38, 45, 55, 81, 96, 120

# - collision events?

# audio = pygame.mixer.Sound("audiotest2.mp3")
# audio.set_volume(0.2)
# audio.play()

import sys
import pygame
import pygame.midi
from gamemanager import GameManager
from imagesdict import ImagesDict
from gamestates.mainmenu import MainMenu
from gameobject import GameObject

# configure screen
SCALE = 4 # pixel width/height -> config

PIXELS = (60, 70) # number of pixels width/height for the screen -> keep here

def main() -> int:
    """Initialize pygame, and run the pet game"""
    # pygame setup
    # https://stackoverflow.com/questions/50569453/why-does-it-say-that-module-pygame-has-no-init-member
    # add "--extension-pkg-whitelist=pygame" to Pylint:Args in Pylint extension settings
    pygame.init()
    pygame.midi.init()
    GameObject.midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())

    # startup screen manager
    gm = GameManager(SCALE, PIXELS)
    ImagesDict.load_resources(gm.drawing_surface) # static function call
    gm.run(MainMenu())

if __name__ == '__main__':
    sys.exit(main())
