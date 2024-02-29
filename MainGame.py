# do game object things instead?
# - meshes (animated / center point, etc)
# - audio sounds
# - on click events, etc
# and initialize the game things before the loop starts
# that is, load images by name (manually) instead of automatically and having a horrible jumble in the loop

# rigidbodies?
# - collision events




# include scenes? - automatically remove all active objects, and add in new objects, with parameters?

import pygame
from gamemanager import GameManager
from gameobject import GameObject
from imagesdict import ImagesDict
from gamestates.room import Room
from gamestates.texttest import TextTest
from gamestates.username import Username
from gamestates.password import Password
from gamestates.roomselector import RoomSelector

# pygame setup
pygame.init()

# debug option
#textDebug = False
# when on, shows text on screen, and can type to write stuff

# configure screen
scale = 4
pixels = (60, 70)
# startup screen manager
gm = GameManager(scale, pixels)
ImagesDict(gm.drawingSurface) # static function call
gm.addState(Username(gm))
gm.addState(TextTest(gm))
gm.addState(Password(gm))
gm.addState(RoomSelector(gm))
gm.addState(Room(gm))

#gm.setState ("texttest")
gm.setState("username") 

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