"""This module contains the code to run the game itself

TODO:
- database stuff


rejection tone
    pitch 35, instrument 6, volume 100
poopy sound
    20/25, 7, 100

    
happiness icon = fullness - poops
when poops, 
    fullness decreases
    when fullness is 0, pet dies
    at 5 poops, pet dies
when eats, 
    fullness increases

when hungry, more squirming than moving
"""
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
from config import Config

PIXELS = (60, 60) # number of pixels width/height for the screen -> keep here

def main() -> int:
    """Initialize pygame, and run the pet game"""
    Config.load_config()

    fps = int(Config.config['Screen']['fps'])
    scale = int(Config.config['Screen']['scale'])

    # pygame setup
    # https://stackoverflow.com/questions/50569453/why-does-it-say-that-module-pygame-has-no-init-member
    # add "--extension-pkg-whitelist=pygame" to Pylint:Args in Pylint extension settings
    pygame.init()
    pygame.midi.init()
    GameObject.midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())

    # startup screen manager
    gm = GameManager(fps, scale, PIXELS)
    ImagesDict.load_resources(gm.drawing_surface) # static function call
    gm.run(MainMenu())

if __name__ == '__main__':
    sys.exit(main())
