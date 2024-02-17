# do game object things instead?
# - meshes (animated / center point, etc)
# - audio sounds
# - on click events, etc
# and initialize the game things before the loop starts
# that is, load images by name (manually) instead of automatically and having a horrible jumble in the loop

# rigidbodies?
# - collision events


import pygame
from os import listdir
from gamemanager import GameManager
from gameobject import GameObject
import random
import imageset

# pygame setup
pygame.init()

# debug option
#textDebug = False
# when on, shows text on screen, and can type to write stuff

# configure screen
scale = 3
pixels = (60, 70)
# startup screen manager
gm = GameManager(scale, pixels)
imageset.setSurface(gm.drawingSurface)
imageset.loadImage("test", [0.5, 0.5], 45, 10)
imageset.loadImage("bgwhite", [0, 0], 1, 0)
imageset.loadImage("room2", [0, 0], 45, 1)
imageset.loadImage("bgblack", [0, 0], 45, 2)

def mainPetOnInit(self):
    self.imgVel = (0, 0)
    self.imgPos = (30, 30)
    self.hiddenPos = (30, 30)

    #self.pos = (30, 30)
    print ("aaa")
    return True
def mainPetOnTick(self, prevPos):
    self.accel = ((random.random() - 0.5)*(0.5 - abs(self.hiddenPos[0]/60 - 0.5)) - ((self.hiddenPos[0]/60 - 0.5)**3)*random.random() ,
             (random.random() - 0.5)*(0.5 - abs(self.hiddenPos[1]/60 - 0.5)) - ((self.hiddenPos[1]/60 - 0.5)**3)*random.random() )
    self.imgVel = (self.imgVel[0]*0.9 + self.accel[0], self.imgVel[1]*0.9 + self.accel[1])
    self.hiddenPos = (self.hiddenPos[0] + self.imgVel[0], self.hiddenPos[1] + self.imgVel[1])
    #uhhh
    if (self.willChangeFrame()):
        return self.hiddenPos
    return prevPos

    

gm.addGameObject(GameObject(imageset.imageSets["test"], onInit = mainPetOnInit, onTick = mainPetOnTick, onReleased = lambda pos: print("AA")))
gm.addGameObject(GameObject(imageset.imageSets["bgwhite"], onInit = lambda self:True, onTick=lambda self, pos:(0, 0)))
gm.addGameObject(GameObject(imageset.imageSets["room2"], onInit = lambda self:True, onTick=lambda self, pos:(0, 0)))
gm.addGameObject(GameObject(imageset.imageSets["bgblack"], onInit = lambda self:True, onTick=lambda self, pos:(0, 0)))

# game loop
running = True

# sprite random movement


# if (textDebug):
#     textDebugString = ""
#     shiftHeld = False

# configure button actions
#gm.images["test"].setClick (print, "AA")

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
            for go in gm.gameObjects:
                if (go.isActive() and go.imageset.contains(go.getCurrentFrame(), pos)):
                    go.released (pos)
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

    for go in gm.gameObjects:
        if (go.isActive()):
            go.tick()

    gm.gameObjects.sort(key=lambda ele:ele.imageset.layer) # so it sorts everything every iteration? maybe. 
    for go in gm.gameObjects:
        if (go.isActive()):
            go.draw()


    #gm.images["bgwhite"].drawImage ()
    #gm.images["room2"].drawImage ((30, 30))
    #gm.drawImage ("bgblack")
    ##sm.images["test"].drawImage ((30, 30))
    #gm.images["test"].drawImage (imgPos)


    # if (textDebug):
    #     gm.drawImage ("bgwhite")
    #     gm.drawText ("ABCDEFGHIJKL", (1, 10), "black", False)
    #     gm.drawText ("MNOPQRSTUVW", (1, 20), "black", False)
    #     gm.drawText ("XYZabcdefghi", (1, 30), "black", False)
    #     gm.drawText ("jklmnopqrstu", (1, 40), "black", False)
    #     gm.drawText ("vwxyz?. a a.a", (1, 50), "black", False)
    #     gm.drawText (textDebugString, (1, 69), "red", False)

    
    #sm.drawImage ("room", (30, 30))
    #sm.drawImage ("kitchen", (30, 30))
    #sm.drawImage ("room2", (30, 30))

    #sm.drawImage ("bgblack")
    #sm.drawImage ("test", imgPos)




    gm.endFrame()
pygame.quit()