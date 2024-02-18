import pygame
import imageset
from gameobject import GameObject
#from imageset import loadImages

# select from choice of filter (1-3)
filterSelection = 2


# frame rate stuff
clock = pygame.time.Clock()
dt = 0

class GameManager:

    def __init__(self, scale, pixels):
        # scale color   alpha
        # 1     255     0
        # 6     50     122
        # 8    0       255
        color = max(255 - (scale - 1) * 50, 0)
        alpha = min((scale - 1) * 20, 255)
        gridColor = (color, color, color, alpha)

        self.scale = scale
        self.pixels = pixels
        screenPixels = (pixels[0]*scale, pixels[1]*scale)
        self.screen = pygame.display.set_mode(screenPixels)
        self.drawingSurface = pygame.Surface (pixels) # surface to draw on with lower resolution than main screen. scaled when drawn onto main screen.
        self.gridfilter = pygame.Surface(screenPixels, pygame.SRCALPHA) #SRCALPHA to make the initial image all transparent (default is all black)
        if (filterSelection == 1 or 3):
            for x in range (0, screenPixels[0], scale):
                pygame.draw.line(self.gridfilter, gridColor, (x, 0), (x, screenPixels[1])) # draw black lines with 100/255 alpha
            for y in range(0, screenPixels[1], scale):
                pygame.draw.line(self.gridfilter, gridColor, (0, y), (screenPixels[0], y))
            if (filterSelection == 3):
                for x in range (0, screenPixels[0] + 1, scale):
                    for y in range(0, screenPixels[1] + 1, scale):
                        pygame.draw.polygon (self.gridfilter, gridColor, [(x - 2, y),(x, y - 2), (x + 2, y), (x, y + 2)])
        if (filterSelection == 2):
            self.gridfilter.fill(gridColor)
            for x in range (int(scale/2), screenPixels[0], scale):
                for y in range(int(scale/2), screenPixels[1], scale):
                    pygame.draw.circle(self.gridfilter, (0, 0, 0, 0), (x, y), scale/2)

        #self.images = loadImages()
        #self.gameObjects = []
        imageset.load(self.drawingSurface)
        self.iObjsDict = {}
        self.iObjsSorted = []
        self.gameObjects = GameManager.GameObjsIterator(self.iObjsSorted)

    class ImageObjects:
        def __init__(self, imageset):
            self.imageset = imageset
            self.gameObjects = []
        def addGameObject (self, obj):
            self.gameObjects.append(obj)
    class GameObjsIterator:
        def __init__(self, iObjsSorted):
            self.iObjsSorted = iObjsSorted
        def __iter__(self):
            self.x = -1 # -1, so that first iteration returns 0
            self.y = 0
            return self
        def __next__(self):
            if (len(self.iObjsSorted) == 0):
                raise StopIteration
            self.x += 1
            if (self.x >= len(self.iObjsSorted[self.y].gameObjects)):
                self.x = 0
                self.y += 1
                if (self.y >= len(self.iObjsSorted)):
                    raise StopIteration
            return self.iObjsSorted[self.y].gameObjects[self.x]

    def addImage (self, name, origin=[0,0], framesEachImage=30):
        imageset.imageSets[name].setImageVariables (origin, framesEachImage)
        iObj = GameManager.ImageObjects(imageset.imageSets[name])

        self.iObjsSorted.append(iObj)
        self.iObjsDict[name] = iObj
        
        
    def addGameObject (self, name, *args, **kwargs):
        go = GameObject(self.iObjsDict[name].imageset, *args, **kwargs)
        self.iObjsDict[name].gameObjects.append(go)


    #def drawImage (self, name, pos=(0, 0)):
    #    self.images[name].drawImage (pos)

    def getLengthOfText (self, string):
        startX = -1 # account for space at the end of the text
        for char in string:
            if (char >= 'a' and char <= 'z'):
                img = self.images ["font" + char + "2"]
            elif (char >= 'A' and char <= 'Z'):
                img = self.images["font" + char]
            elif (char == "."):
                img = self.images["fontdot"]
            elif (char == "?"):
                img = self.images["fontquestion"]
            elif (("font" + char) in self.images):
                img = self.images["font" + char]
            else:
                print ("Cannot find character: ", char)
            startX += img[0].get_width() + 1 # 1 space in-between characters
        return startX
    
    def drawText (self, string, pos, color=(0, 0, 0, 255), centered = True): # if not centered, then left-aligned
        # calculate length
        if (centered):
            startX = -int(self.getLengthOfText(string) / 2) # round up or down? does it matter?
        else:
            startX = 0
        for char in string:
            if (char >= 'a' and char <= 'z'):
                img = self.images ["font" + char + "2"]
            elif (char >= 'A' and char <= 'Z'):
                img = self.images["font" + char]
            elif (char == "."):
                img = self.images["fontdot"]
            elif (char == "?"):
                img = self.images["fontquestion"]
            elif (("font" + char) in self.images):
                img = self.images["font" + char]

            if (color is not (0, 0, 0, 255)):
                copy = img[0].copy() # required for custom colors....? would it be just faster to do <...>.. yeah, but eh
                copy.fill(color, special_flags=pygame.BLEND_MAX)
            
            #img.drawImage ((pos[0] + startX, pos[1]))
            self.drawingSurface.blit (copy, #blargh
                                    (pos[0] + startX - img.origin[0] * img[0].get_width(), 
                                    pos[1] - img.origin[1] * img[0].get_height())
                                    )
            
            startX += img[0].get_width() + 1 # uh huh



    #def drawImage (self, imageName, pos=(0, 0)): # frames? auto-detect duration on screen / number of draw calls?
        #drawSurface.blit (allImages[imageName][frame], pos)
    #    self.allImages[imageName].drawImage (self.drawingSurface, pos)
        #drawingSurface.blit (img, (imgPos[0] - 15, imgPos[1] - 15))

    #def handleMouse (self, pos):
    #    for imageSet in self.images.values():
    #        if (imageSet.clickable and imageSet.contains (pos)):
    #            if debug:
    #                print ("Clicked on ", imageSet.name)
    #            imageSet.onClick()

    def endFrame(self):
        # for imgSet in self.images.values():
        #     if not imgSet.wasUsedThisFrame: # reset animation if it wasn't on the screen last frame
        #         imgSet.currentFrame = 0
        #     else:
        #         imgSet.wasUsedThisFrame = False # reset frame tracker
        # draw drawingSurface (small pixel screen) onto main screen after multiplying its scale
        self.screen.blit (pygame.transform.scale_by(self.drawingSurface, self.scale), (0, 0)) #
        #filter
        self.screen.blit(self.gridfilter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()

        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000