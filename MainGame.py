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
from gamestates.room2 import Room2

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
gm.addState(Room(gm))
gm.addState(Room2(gm))

gm.setState("room") # set first state (will be "login screen" in the future)

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
        #elif event.type == pygame.KEYDOWN:
        #    #if textDebug:
        #    asText = pygame.key.name(event.key)
        #    print (asText)
        #    if (asText.isalpha() and len(asText) == 1):
        #        if (shiftHeld):
        #            textDebugString += asText.capitalize()
        #        else:
        #            textDebugString += asText
        #    elif shiftHeld and asText in ['/']:
        #        if asText == '/':
        #            textDebugString += '?'
        #    elif asText in ['.']:
        #        textDebugString += asText
        #    elif asText == 'space':
        #        textDebugString += ' '
        #    elif asText == 'left shift' or asText == 'right shift':
        #        shiftHeld = True
        #    elif asText == 'backspace':
        #        textDebugString = textDebugString[:-1] # https://stackoverflow.com/questions/15478127/remove-final-character-from-string
        #elif event.type == pygame.KEYUP:
        #    if textDebug:
        #        if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
        #            shiftHeld = False

    gm.handleTick()
    gm.handleMeshes()

    gm.endFrame()
pygame.quit()