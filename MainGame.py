# Example file showing a circle moving on screen
import pygame
from os import listdir
from screenmanager import ScreenManager
import random

# pygame setup
pygame.init()


scale = 5
pixels = (60, 70)
sm = ScreenManager(scale, pixels)

running = True


imgVel = (0, 0)
imgPos = (30, 30)
hiddenPos = (30, 30)


sm.images["test"].setClick (print, "AA")

while running:
    # poll for events
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if (pos):
            pos = (int(pos[0]/scale), int(pos[1]/scale))
        #print (pos)
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    if abs(pos[0] - imgPos[0]) < 5 and abs(pos[1] - imgPos[1]) < 5:
        #        dragged = True
        #elif event.type == pygame.MOUSEMOTION:
        #    if dragged:
        #        imgPos = (pos[0], pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            sm.handleMouse(pos)
            #if dragged:
            #    dragged = False

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
    sm.images["bgblack"].drawImage ()
    #sm.images["test"].drawImage ((30, 30))
    sm.images["test"].drawImage (imgPos)
    
    #sm.drawImage ("room", (30, 30))
    #sm.drawImage ("kitchen", (30, 30))
    #sm.drawImage ("room2", (30, 30))

    #sm.drawImage ("bgblack")
    #sm.drawImage ("test", imgPos)




    sm.endFrame()
pygame.quit()