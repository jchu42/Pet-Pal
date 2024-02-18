from os import listdir
import pygame

# debug option
debug = False

class ImageSet:
    def __init__ (self, name, surface):
        self.name = name
        self.images = {}
        if ("font" in name):
            self.origin = [0, 1] # bottom left for text
        else:
            self.origin = [0.5, 0.5] # default middle middle
        self.framesEachImage = 30 # lower for faster, higher for slower - default 30 frames per image
        #self.layer = 5
        # self.currentFrame = 0
        # self.wasUsedThisFrame = False
        #self.clickable = False # to prevent clicks not going through (user can only click on one object)
        #self.func = 0
        #self.args = 0
        #self.wargs = 0
        self.surface = surface
        #self.pos = (0, 0)
    def __getitem__ (self, pos):
        return self.images[pos]
    def drawImage (self, pos=(0, 0), frame=0):
        self.pos = pos
        self.surface.blit (self[frame], 
                                (pos[0] - self.origin[0] * self[frame].get_width(), 
                                pos[1] - self.origin[1] * self[frame].get_height())
                                )
        self.wasUsedThisFrame = True

    def setImageVariables (self, origin=[0,0], framesEachImage=30):
        if ("middle" in origin):
            o = [0.5,0.5]
        else:
            o = [-1, -1]
        if ("left" in origin):
            o = [0, o[1]]
        elif ("right" in origin):
            o = [1, o[1]]
        if ("top" in origin):
            o = [o[0], 0]
        elif ("bottom" in origin):
            o = [o[0], 1]
        if (o == [-1, -1]):
            self.origin = origin # uwu
        else:
            self.origin = o
        self.framesEachImage = framesEachImage
    #def willChangeFrame (self):
    #    return self.currentFrame % self.framesEachImage == self.framesEachImage - 1
        
    #def setClick (self, function, *args, **wargs):
    #    self.clickable = True
    #    self.func = function
    #    self.args = args
    #    self.wargs = wargs
    #def onClick (self):
    #    self.func(*self.args, **self.wargs)

imageSets = {}
def load(surface):
    files = listdir("images/") # assuming all are files
    #imageDataFile = ""
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
            if name not in imageSets:
                imageSets[name] = ImageSet(name, surface)
            imageSets[name].images [num] = pygame.image.load("images/" + filename).convert_alpha()
            

