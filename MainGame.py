
# TODO:
# - database (store username/password, statuses, last time)
# - eating
# - cleaning up poop animation
# - hunger/health levels; display status
# - combine username and password states; add a back button to go from password back to username

# cool instruments:
# 10, 32/34, 38, 46, 55, 81, 96, 120

# - collision events?

import pygame
import pygame.midi
from gamemanager import GameManager
from gameobject import GameObject
from imagesdict import ImagesDict
from gamestates.room import Room
from gamestates.texttest import TextTest
from gamestates.login import Login
from gamestates.roomselector import RoomSelector
from gamestates.petselector import PetSelector
from gamestates.audiotest import AudioTest
from gamestates.mainmenu import MainMenu

# pygame setup
pygame.init()
pygame.midi.init()
# audio = pygame.mixer.Sound("audiotest2.mp3")
# audio.set_volume(0.2)
#audio.play()


# configure screen
scale = 4
pixels = (60, 70)
# startup screen manager
gm = GameManager(scale, pixels)
ImagesDict(gm.drawingSurface) # static function call
gm.addState(Login(gm))
gm.addState(TextTest(gm))
gm.addState(RoomSelector(gm))
gm.addState(PetSelector(gm))
gm.addState(Room(gm))
gm.addState(AudioTest(gm))
gm.addState(MainMenu(gm))

gm.setState("mainmenu") # login screen

# game loop
running = True
while running:
    # poll for events
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if (pos):
            pos = (int(pos[0]/scale), int(pos[1]/scale))
            gm.handleMouseHover(pos)
        if event.type == pygame.QUIT:
            gm.resetHandlers() # calls on delete for active objects if needed?
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            gm.handleMouseUp(pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gm.handleMouseDown(pos)
        elif event.type == pygame.MOUSEMOTION:
            gm.handleMouseHover(pos)
        elif event.type == pygame.KEYDOWN:
            gm.handleKeyPress(pygame.key.name(event.key))

    gm.handleTick()
    gm.handleMeshes()

    gm.endFrame()
pygame.quit()