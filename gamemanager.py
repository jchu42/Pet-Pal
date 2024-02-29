import pygame
from imagesdict import ImagesDict
from typing import Self
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
        self.screenPixels = (pixels[0]*scale, pixels[1]*scale)
        self.screen = pygame.display.set_mode(self.screenPixels)
        self.drawingSurface = pygame.Surface (pixels) # surface to draw on with lower resolution than main screen. scaled when drawn onto main screen.
        self.gridfilter = self.__generateGridSurface(scale, self.screenPixels)

        #self.images = loadImages()
        #self.gameObjects = []
        ImagesDict.loadResources(self.drawingSurface)


        self.newState = 0
        #self.onStateChange = None # define in MainGame
        self.states = {}
        self.currentState = ""
        self.stateChanged = True
        self.gos = []
        self.goMouseHover = [] # separate array for each object allows us to have a tonne of objects with less overhead?
        self.goMouseDown = []
        self.goMouseDrag = []
        self.goMouseUp = []
        self.onDelete = []
        self.onKeyPress = []

    def addState (self, state: gamestate)->Self:
        self.states[state.getName()] = state
        return self

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
        for function in self.onDelete:
            function()
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
        self.onKeyPress = []

    def addGameObject (self, go:GameObject)->GameObject:
        self.gos.append(go)
        return go
    def removeGameObject(self, go:GameObject)->GameObject:
        if go in self.gos:
            self.gos.remove(go)
        for tup in self.goMouseHover:
            if (tup[0] == go):
                self.goMouseHover.remove(tup)
        for tup in self.goMouseDown:
            if (tup[0] == go):
                self.goMouseDown.remove(tup)
        for tup  in self.goMouseDrag:
            if (tup[0] == go):
                self.goMouseDrag.remove(tup)
        for tup in self.goMouseUp:
            if (tup[0] == go):
                self.goMouseUp.remove(tup)
        for tup in self.onDelete:
            if (tup[0] == go):
                tup[1](tup[0]) # AHAHAAHA
                self.onDelete.remove(tup)

    def handleTick(self)->None:
        if (self.currentState != ''):
            self.states[self.currentState].stateTick()
        for go in self.gos:
            go.tick()
    
    def handleMeshes(self)->None:
        for go in self.gos:
            go.draw()

    def assignMouseHover (self, go, function)->GameObject:
        self.goMouseHover.append((go, function))
        return go
    def handleMouseHover (self, pos):
        # object must have a mesh
        for go, function in self.goMouseHover:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(pos)

    def assignMouseDown (self, go:GameObject, function) -> GameObject:
        self.goMouseDown.append((go, function))
        return go
    def handleMouseDown (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDown:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(pos)

    def assignMouseDrag (self, go:GameObject, function) -> GameObject:
        self.goMouseDrag.append((go, function))
        return go
    def handleMouseDrag (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDrag:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(pos)

    def assignMouseUp (self, go:GameObject, function) -> GameObject:
        self.goMouseUp.append((go, function))
        return go
    def handleMouseUp (self, pos):
        # object must have a mesh
        for go, function in self.goMouseUp:
            if (go.contains ((pos[0] - go.getPos()[0], pos[1] - go.getPos()[1]))):
                function(pos)

    def assignDelete (self, go:GameObject, function) -> GameObject:
        self.onDelete.append((go, function))
        return go

    def assignKeyPress (self, go:GameObject, function)->GameObject:
        self.onKeyPress.append((go, function))
        return go
    def handleKeyPress(self, str)->None:
        for go, function in self.onKeyPress:
            function(str)

    def setState (self, newState:str, *args, **kwargs)->None:
        self.newState = newState
        self.stateChanged = True
        self.args = args
        self.kwargs = kwargs

    def endFrame(self)->None:
        # draw scaled drawing surface to screen buffer
        self.screen.blit (pygame.transform.scale_by(self.drawingSurface, self.scale), (0, 0)) 
        # draw filter
        self.screen.blit(self.gridfilter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        #dt = clock.tick(60) / 1000
        clock.tick(fps)

        if (self.stateChanged):
            self.currentState = self.newState
            self.stateChanged = False
            # reset manager
            self.resetHandlers()
            #self.onStateChange(self, self.state, self.args, self.kwargs)
            self.states[self.currentState].loadState(*self.args, **self.kwargs)