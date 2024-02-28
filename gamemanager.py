import pygame
from imagesdict import ImagesDict
import gameobject as GameObject
import gamestate
#from imageset import loadImages

# select from choice of filter (1-3)
filterSelection = 2

#gameobjects only exist in component handlers

# frame rate stuff
fps = 5
clock = pygame.time.Clock()
dt = 0

class GameManager:

    def __init__(self, scale: int, pixels:tuple[int, int])->None:

        self.scale = scale
        self.pixels = pixels
        screenPixels = (pixels[0]*scale, pixels[1]*scale)
        self.screen = pygame.display.set_mode(screenPixels)
        self.drawingSurface = pygame.Surface (pixels) # surface to draw on with lower resolution than main screen. scaled when drawn onto main screen.
        self.gridfilter = self.__generateGridSurface(scale, screenPixels)

        #self.images = loadImages()
        #self.gameObjects = []
        ImagesDict.loadResources(self.drawingSurface)


        self.newState = 0
        #self.onStateChange = None # define in MainGame
        self.states = {}
        self.state = 0
        self.stateChanged = True
        self.gos = []
        self.goMouseHover = [] # separate array for each object allows us to have a tonne of objects with less overhead?
        self.goMouseDown = []
        self.goMouseDrag = []
        self.goMouseUp = []
        self.onDelete = []

    def addState (self, state: gamestate):
        self.states[state.getName()] = state

    def __generateGridSurface(self, scale:int, screenPixels: tuple[int, int])->pygame.Surface:
        color = max(255 - (scale - 1) * 50, 0)
        alpha = min((scale - 1) * 20, 255)
        gridColor = (color, color, color, alpha)
        gridfilter = pygame.Surface(screenPixels, pygame.SRCALPHA) #SRCALPHA to make the initial image all transparent (default is all black)
        if (filterSelection == 1 or 3):#put into another function!!!
                for x in range (0, screenPixels[0], scale):
                    pygame.draw.line(gridfilter, gridColor, (x, 0), (x, screenPixels[1])) # draw black lines with 100/255 alpha
                for y in range(0, screenPixels[1], scale):
                    pygame.draw.line(gridfilter, gridColor, (0, y), (screenPixels[0], y))
                if (filterSelection == 3):
                    for x in range (0, screenPixels[0] + 1, scale):
                        for y in range(0, screenPixels[1] + 1, scale):
                            pygame.draw.polygon (gridfilter, gridColor, [(x - 2, y),(x, y - 2), (x + 2, y), (x, y + 2)])
        if (filterSelection == 2):
            gridfilter.fill(gridColor)
            for x in range (int(scale/2), screenPixels[0], scale):
                for y in range(int(scale/2), screenPixels[1], scale):
                    pygame.draw.circle(gridfilter, (0, 0, 0, 0), (x, y), scale/2)
        return gridfilter
    
    # def createMesh (self, name, origin=[0,0], framesEachImage=30):
    #     imageset.imageSets[name].setImageVariables (origin, framesEachImage)
    #     iObj = GameManager.Mesh(imageset.imageSets[name])
    #     self.goMeshes.append(iObj)
    #     self.goMeshesDict[name] = iObj

    def resetHandlers (self)->None:
        for go, function in self.onDelete:
            function(go)
        self.onDelete = []
        # for gomesh in self.goMeshes:
        #     gomesh.gameObjects = []
        # self.goMeshes = []
        # self.goTick = []
        self.gos = []
        self.goMouseHover = []
        self.goMouseDown = []
        self.goMouseDrag = []
        self.goMouseUp = []

    def addGameObject (self, go:GameObject)->GameObject:
        self.gos.append(go)
        return go

    def handleTick(self)->None:
        for go in self.gos:
            go.tick()
    
    def handleMeshes(self)->None:
        for go in self.gos:
            go.draw()

    def assignMouseHover (self, go:GameObject, function)->GameObject:
        self.goMouseHover.append((go, function))
        return go
    def handleMouseHover (self, pos):
        # object must have a mesh
        for go, function in self.goMouseHover:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(go, pos)

    def assignMouseDown (self, go:GameObject, function) -> GameObject:
        self.goMouseDown.append((go, function))
        return go
    def handleMouseDown (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDown:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(go, pos)

    def assignMouseDrag (self, go:GameObject, function) -> GameObject:
        self.goMouseDrag.append((go, function))
        return go
    def handleMouseDrag (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDrag:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(go, pos)

    def assignMouseUp (self, go:GameObject, function) -> GameObject:
        self.goMouseUp.append((go, function))
        return go
    def handleMouseUp (self, pos):
        # object must have a mesh
        for go, function in self.goMouseUp:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(go, pos)

    def assignDelete (self, go:GameObject, function) -> GameObject:
        self.onDelete.append((go, function))
        return go

    
    # def assignText (self, go, string, color=(0, 0, 0, 255), centered = True): # if not centered, then left-aligned
    #     name = "TEXT" + ' '.join(map(str, color)) + string + str(centered) # save all copies of colors of strings of text
    #     if (name) not in imagesdict.imageSets:
    #         textSurface = pygame.Surface((self.__getLengthOfText (string), 8), pygame.SRCALPHA) # how tall is the text anyway?
            
    #         startX = 0 # round up or down? does it matter?

    #         for char in string:
    #             if (char >= 'a' and char <= 'z'):
    #                 img = imagesdict.imageSets ["font" + char + "2"]
    #             elif (char >= 'A' and char <= 'Z'):
    #                 img = imagesdict.imageSets["font" + char]
    #             elif (char == "."):
    #                 img = imagesdict.imageSets["fontdot"]
    #             elif (char == "?"):
    #                 img = imagesdict.imageSets["fontquestion"]
    #             elif (("font" + char) in imagesdict.imageSets):
    #                 img = imagesdict.imageSets["font" + char]
    #             else:
    #                 print ("char", char, "not found")

    #             if (color is not (0, 0, 0, 255)):
    #                 copy = img[0].copy() # required for custom colors....? would it be just faster to do <...>.. yeah, but eh
    #                 copy.fill(color, special_flags=pygame.BLEND_MAX)
    #             else:
    #                 copy = img[0]

    #             textSurface.blit (copy, (startX - img.origin[0] * img[0].get_width(), 0))

    #             startX += img[0].get_width() + 1 # uh huh
            
    #         imagesdict.imageSets [name] = imagesdict.ImageSet(name, self.drawingSurface)
    #         imagesdict.imageSets [name].images[0] = textSurface
    #         if (centered):
    #             self.createMesh (name, origin=[0.5,1], framesEachImage = 1)
    #         else:
    #             self.createMesh (name, origin=[0,1], framesEachImage = 1)
    #     #self.assignMesh (go, name)
    #     go.setImageName(name)


    def setState (self, newState:str, *args, **kwargs)->None:
        self.newState = newState
        self.stateChanged = True
        self.args = args
        self.kwargs = kwargs

    def endFrame(self)->None:
        self.screen.blit (pygame.transform.scale_by(self.drawingSurface, self.scale), (0, 0)) # draw scaled drawing surface to screen buffer
        #filter
        self.screen.blit(self.gridfilter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()

        
        
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        #dt = clock.tick(60) / 1000
        clock.tick(fps) / 1000

        if (self.stateChanged):
            self.state = self.newState
            self.stateChanged = False
            # reset manager
            self.resetHandlers()
            #self.onStateChange(self, self.state, self.args, self.kwargs)
            self.states[self.state].loadState()