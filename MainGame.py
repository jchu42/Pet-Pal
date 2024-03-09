"""This module contains the code to run the game itself"""

import sys
import pygame
import pygame.midi
from gamemanager import GameManager
from imagesdict import ImagesDict
from gamestates.mainmenu import MainMenu
from gameobject import GameObject
from config import Config

PIXELS = (60, 60) # number of pixels width/height for the screen

def main() -> int:
    """Initialize pygame, and run the pet game"""
    Config.load_config()

    fps = int(Config.config['Screen']['fps'])
    scale = int(Config.config['Screen']['scale'])

    # pygame setup
    # https://stackoverflow.com/questions/50569453/why-does-it-say-that-module-pygame-has-no-init-member
    # add "--extension-pkg-whitelist=pygame" to Pylint:Args in Pylint extension settings
    pygame.init()
    pygame.display.set_caption('Pet Pal')
    pygame.midi.init()
    GameObject.midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())
    pygame.mixer.music.load('Sakura-Girl-Lucky-Day.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    # startup screen manager
    gm = GameManager(fps, scale, PIXELS)
    ImagesDict.load_resources(gm.drawing_surface) # static function call
    gm.run(MainMenu())

if __name__ == '__main__':
    sys.exit(main())
