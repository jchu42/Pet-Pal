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
from os import listdir
from gamemanager import GameManager
from gameobject import GameObject
import random

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
gm.createMesh("bgwhite", [0, 0], 1) # order matters - later images are drawn on top
gm.createMesh("room2", [0, 0], 1)
gm.createMesh("bgblack", [0, 0], 1)
gm.createMesh("test", [0.5, 0.5], 45)


def handleStateChange (state, *args, **kwargs): # arbitrary argument input for game state customization
    if (state == 0):
        # define game object behaviors
        def mainPetOnInit(self):
            self.imgVel = (0, 0)
            self.imgPos = (30, 30)
            self.hiddenPos = (30, 30)
            return True
        def mainPetOnTick(self, prevPos):
            self.accel = ((random.random() - 0.5)*(0.5 - abs(self.hiddenPos[0]/60 - 0.5)) - ((self.hiddenPos[0]/60 - 0.5)**3)*random.random() ,
                    (random.random() - 0.5)*(0.5 - abs(self.hiddenPos[1]/60 - 0.5)) - ((self.hiddenPos[1]/60 - 0.5)**3)*random.random() )
            self.imgVel = (self.imgVel[0]*0.9 + self.accel[0], self.imgVel[1]*0.9 + self.accel[1])
            self.hiddenPos = (self.hiddenPos[0] + self.imgVel[0], self.hiddenPos[1] + self.imgVel[1])
            if (self.willChangeFrame()):
                return self.setPos (self.hiddenPos)
        def mainPetOnClick (self, pos):
            print ("AA")
        mainPet = GameObject ()
        gm.assignMesh(mainPet, "test")
        gm.assignInit(mainPet, mainPetOnInit)
        gm.assignTick(mainPet, mainPetOnTick)
        gm.assignMouseUp(mainPet, mainPetOnClick)

        def mainUI():
            bgwhite = GameObject()
            gm.assignMesh(bgwhite, "bgwhite")
            room2 = GameObject()
            gm.assignMesh(room2, "room2")
            bgblack = GameObject()
            gm.assignMesh(bgblack, "bgblack")
        mainUI()
        # define game objects
        #gm.addGameObject("bgwhite", onInit = lambda self:True, onTick=lambda self, pos:(0, 0))
        #gm.addGameObject("room2", onInit = lambda self:True, onTick=lambda self, pos:(0, 0))
        #gm.addGameObject("bgblack", onInit = lambda self:True, onTick=lambda self, pos:(0, 0))
        #gm.addGameObject("test", onInit = mainPetOnInit, onTick = mainPetOnTick, onReleased = lambda pos: print("AA"))
gm.onStateChange = handleStateChange

# game loop
running = True
while running:

    # poll for events
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if (pos):
            pos = (int(pos[0]/scale), int(pos[1]/scale))
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            #gm.handleMouse(pos)
            #for go in gm.gameObjects:
            #    if (go.isActive() and go.contains(pos)):
            #        go.released (pos)
            gm.handleMouseUp(pos)
        elif event.type == pygame.KEYDOWN:
            if textDebug:
                asText = pygame.key.name(event.key)
                print (asText)
                if (asText.isalpha() and len(asText) == 1):
                    if (shiftHeld):
                        textDebugString += asText.capitalize()
                    else:
                        textDebugString += asText
                elif shiftHeld and asText in ['/']:
                    if asText == '/':
                        textDebugString += '?'
                elif asText in ['.']:
                    textDebugString += asText
                elif asText == 'space':
                    textDebugString += ' '
                elif asText == 'left shift' or asText == 'right shift':
                    shiftHeld = True
                elif asText == 'backspace':
                    textDebugString = textDebugString[:-1] # https://stackoverflow.com/questions/15478127/remove-final-character-from-string
        elif event.type == pygame.KEYUP:
            if textDebug:
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    shiftHeld = False

    gm.handleTick()
    gm.handleMeshes()
    #for go in gm.gameObjects:
    #    if (go.isActive()):
    #        go.tick()
#
    #for go in gm.gameObjects:
    #    if (go.isActive()):
    #        go.draw()

    gm.endFrame()
pygame.quit()