# Example file showing a circle moving on screen
import pygame
from os import listdir
from screenmanager import ScreenManager
import random

# pygame setup
pygame.init()

# debug option
textDebug = True
# when on, shows text on screen, and can type to write stuff

# configure screen
scale = 5
pixels = (60, 70)
# startup screen manager
sm = ScreenManager(scale, pixels)

# game loop
running = True

# sprite random movement
imgVel = (0, 0)
imgPos = (30, 30)
hiddenPos = (30, 30)

if (textDebug):
    textDebugString = ""
    shiftHeld = False

# configure button actions
sm.images["test"].setClick (print, "AA")

while running:
    # poll for events
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if (pos):
            pos = (int(pos[0]/scale), int(pos[1]/scale))
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            sm.handleMouse(pos)
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

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    accel = ((random.random() - 0.5)*(0.5 - abs(hiddenPos[0]/60 - 0.5)) - ((hiddenPos[0]/60 - 0.5)**3)*random.random() ,
             (random.random() - 0.5)*(0.5 - abs(hiddenPos[1]/60 - 0.5)) - ((hiddenPos[1]/60 - 0.5)**3)*random.random() )
    imgVel = (imgVel[0]*0.9 + accel[0], imgVel[1]*0.9 + accel[1])
    hiddenPos = (hiddenPos[0] + imgVel[0], hiddenPos[1] + imgVel[1])
    #uhhh
    if (sm.images["test"].willChangeFrame()):
        imgPos = hiddenPos


    sm.images["bgwhite"].drawImage ()
    sm.images["room2"].drawImage ((30, 30))
    sm.drawImage ("bgblack")
    #sm.images["test"].drawImage ((30, 30))
    sm.images["test"].drawImage (imgPos)


    if (textDebug):
        sm.drawImage ("bgwhite")
        sm.drawText ("ABCDEFGHIJKL", (1, 10), "black", False)
        sm.drawText ("MNOPQRSTUVW", (1, 20), "black", False)
        sm.drawText ("XYZabcdefghi", (1, 30), "black", False)
        sm.drawText ("jklmnopqrstu", (1, 40), "black", False)
        sm.drawText ("vwxyz?. a a.a", (1, 50), "black", False)
        sm.drawText (textDebugString, (1, 69), "red", False)

    
    #sm.drawImage ("room", (30, 30))
    #sm.drawImage ("kitchen", (30, 30))
    #sm.drawImage ("room2", (30, 30))

    #sm.drawImage ("bgblack")
    #sm.drawImage ("test", imgPos)




    sm.endFrame()
pygame.quit()