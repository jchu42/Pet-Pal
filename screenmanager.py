import pygame
from os import listdir

debug = True
filterSelection = 2


clock = pygame.time.Clock()
dt = 0

class ScreenManager:

    def __init__(self, scale, pixels):
        gridColor = (50, 50, 50, 100)

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

        self.images = self.__loadImages__()

    class ImageSet:
        def __init__ (self, name, surface):
            self.name = name
            self.images = {}
            self.origin = [0.5, 0.5] # default middle middle
            self.framesEachImage = 30 # lower for faster, higher for slower - default 30 frames per image
            self.currentFrame = 0
            self.wasUsedThisFrame = False
            self.clickable = False # to prevent clicks not going through (user can only click on one object)
            self.func = 0
            self.args = 0
            self.wargs = 0
            self.surface = surface
            self.pos = (0, 0)
        def __getitem__ (self, pos):
            return self.images[pos]
        def drawImage (self, pos=(0, 0)):
            self.pos = pos
            self.currentFrame += 1
            frame = int (self.currentFrame / self.framesEachImage) % len(self.images)
            self.surface.blit (self[frame], 
                                    (pos[0] - self.origin[0] * self[frame].get_width(), 
                                    pos[1] - self.origin[1] * self[frame].get_height())
                                    )
            self.wasUsedThisFrame = True

        def willChangeFrame (self):
            return self.currentFrame % self.framesEachImage == self.framesEachImage - 1
        def setClick (self, function, *args, **wargs):
            self.clickable = True
            self.func = function
            self.args = args
            self.wargs = wargs
        def onClick (self):
            self.func(*self.args, **self.wargs)
        def contains (self, pos):
            # calculate bounding box
            frame = int (self.currentFrame / self.framesEachImage) % len(self.images)
            left = self.pos[0] - self.origin[0] * self[frame].get_width() - 1 # hueh?
            top = self.pos[1] - self.origin[1] * self[frame].get_height() - 1 
            right = self.pos[0] + (1 - self.origin[0]) * self[frame].get_width()
            bottom = self.pos[1] + (1 - self.origin[1]) * self[frame].get_height()
            return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)


    def __loadImages__(self):
        images = {}
        files = listdir("images/") # assuming all are files
        imageDataFile = ""
        for filename in files:
            # https://stackoverflow.com/questions/4444923/get-filename-without-extension-in-python
            splitName = filename.split (".")
            if debug:
                print (splitName)
            name = splitName[0]
            if (len(splitName) == 2):
                num = 0
                type = splitName[1]
            else:
                num = int(splitName[1])
                type = splitName[2]
            if type == "png" or type == "jpg":
                #print (name)
                if name not in images:
                    images[name] = self.ImageSet(name, self.drawingSurface)
                images[name].images [num] = pygame.image.load("images/" + filename).convert_alpha()
            elif type == "txt":
                #image data
                imageDataFile = filename
        for text in map (lambda line: line.split(" "), open("images/" + imageDataFile)):
            if debug:
                print (text)
            if text[0] in images:
                match text[2]: # "top left" means y coordinate, then x coordinate
                    case "left":
                        images[text[0]].origin[0] = 0
                    case "middle":
                        images[text[0]].origin[0] = 0.5
                    case "right":
                        images[text[0]].origin[0] = 1
                    case _:
                        print ("Invalid position: ", text[2])
                match text[1]:
                    case "top":
                        images[text[0]].origin[1] = 0
                    case "middle":
                        images[text[0]].origin[1] = 0.5
                    case "bottom":
                        images[text[0]].origin[1] = 1
                    case _:
                        print ("Invalid position: ", text[1])

                #images[text[0]].origin = (float(text[1]), float(text[2]))
                images[text[0]].framesEachImage = int(text[3])
            else:
                print ("Warning: image ", text[0], " not found!")
            # ignore if not in images list
        return images

    #def drawImage (self, imageName, pos=(0, 0)): # frames? auto-detect duration on screen / number of draw calls?
        #drawSurface.blit (allImages[imageName][frame], pos)
    #    self.allImages[imageName].drawImage (self.drawingSurface, pos)
        #drawingSurface.blit (img, (imgPos[0] - 15, imgPos[1] - 15))

    def handleMouse (self, pos):
        for imageSet in self.images.values():
            if (imageSet.clickable and imageSet.contains (pos)):
                if debug:
                    print ("Clicked on ", imageSet.name)
                imageSet.onClick()

    def endFrame(self):
        for imgSet in self.images.values():
            if not imgSet.wasUsedThisFrame: # reset animation if it wasn't on the screen last frame
                imgSet.currentFrame = 0
            else:
                imgSet.wasUsedThisFrame = False # reset frame tracker
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

        
        #for event in pygame.event.get():
        #     pos = pygame.mouse.get_pos()
        #     if (pos):
        #         pos = (int(pos[0]/scale), int(pos[1]/scale))
        #     #print (pos)
            #if event.type == pygame.QUIT:
             #   running = False
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         if abs(pos[0] - imgPos[0]) < 5 and abs(pos[1] - imgPos[1]) < 5:
        #             dragged = True
        #     elif event.type == pygame.MOUSEMOTION:
        #         if dragged:
        #             imgPos = (pos[0], pos[1])
        #     elif event.type == pygame.MOUSEBUTTONUP:
        #         if dragged:
        #             dragged = False
