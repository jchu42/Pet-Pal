import pygame
import imageset
from gameobject import GameObject
#from imageset import loadImages

# select from choice of filter (1-3)
filterSelection = 2

#gameobjects only exist in component handlers

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


        self.newState = 0
        self.onStateChange = None # define in MainGame
        self.state = 0
        self.stateChanged = True
        self.args = ()
        self.kwargs = ()
        self.goMeshesDict = {}
        self.goMeshes = []
        self.goTick = []
        self.goMouseHover = [] # separate array for each object allows us to have a tonne of objects with less overhead?
        self.goMouseDown = []
        self.goMouseDrag = []
        self.goMouseUp = []
    
    
    def createMesh (self, name, origin=[0,0], framesEachImage=30):
        imageset.imageSets[name].setImageVariables (origin, framesEachImage)
        iObj = GameManager.Mesh(imageset.imageSets[name])
        self.goMeshes.append(iObj)
        self.goMeshesDict[name] = iObj

    def resetHandlers (self):
        for gomesh in self.goMeshes:
            gomesh.gameObjects = []
        self.goTick = []
        self.goMouseHover = []
        self.goMouseDown = []
        self.goMouseDrag = []
        self.goMouseUp = []

    class Mesh:
        def __init__(self, imageset):
            self.imageset = imageset
            self.gameObjects = []
        def addGameObject (self, obj):
            self.gameObjects.append(obj)
    def assignMesh (self, go, name):
        if (name not in self.goMeshesDict):
            print ("Image", name, "not found. Did you forget to createMesh (" + name + ") it?")
        self.goMeshesDict[name].gameObjects.append(go)
        go.name = name
        go.framesEachImage = self.goMeshesDict[name].imageset.framesEachImage
        go.images = self.goMeshesDict[name].imageset.images
    def handleMeshes(self):
        for gomesh in self.goMeshes:
            for go in gomesh.gameObjects:
                if (go.active):
                    go.pos = go.nextPos
                    gomesh.imageset.drawImage(go.pos, go.getCurrentFrame())
                    go.currentFrame += 1

    def assignInit (self, go, function):
        function(go) # lmao

    def assignTick (self, go, function):
        self.goTick.append  ((go, function))
    def handleTick (self):
        for go, function in self.goTick:
            if (go.active):
                function(go, go.pos)

    def assignMouseHover (self, go, function):
        self.goMouseHover.append((go, function))
    def handleMouseHover (self, pos):
        # object must have a mesh
        for go, function in self.goMouseHover:
            if (go.active and go.name in self.goMeshesDict):
                # use mesh's dimensions to detect if it's inside
                if (self.goMeshesDict[go.name].imageset.contains (go.getCurrentFrame(), (pos[0] - go.pos[0], pos[1] - go.pos[1]))):
                    function(go, pos)

    def assignMouseDown (self, go, function):
        self.goMouseDown.append((go, function))
    def handleMouseDown (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDown:
            if (go.active and go.name in self.goMeshesDict):
                # use mesh's dimensions to detect if it's inside
                if (self.goMeshesDict[go.name].imageset.contains (go.getCurrentFrame(), (pos[0] - go.pos[0], pos[1] - go.pos[1]))):
                    function(go, pos)

    def assignMouseDrag (self, go, function):
        self.goMouseDrag.append((go, function))
    def handleMouseDrag (self, pos):
        # object must have a mesh
        for go, function in self.goMouseDrag:
            if (go.active and go.name in self.goMeshesDict):
                # use mesh's dimensions to detect if it's inside
                if (self.goMeshesDict[go.name].imageset.contains (go.getCurrentFrame(), (pos[0] - go.pos[0], pos[1] - go.pos[1]))):
                    function(go, pos)

    def assignMouseUp (self, go, function):
        self.goMouseUp.append((go, function))
    def handleMouseUp (self, pos):
        # object must have a mesh
        for go, function in self.goMouseUp:
            if (go.active and go.name in self.goMeshesDict):
                # use mesh's dimensions to detect if it's inside
                if (self.goMeshesDict[go.name].imageset.contains (go.getCurrentFrame(), (pos[0] - go.pos[0], pos[1] - go.pos[1]))):
                    function(go, pos)

    def __getLengthOfText (self, string):
        startX = -1 # account for space at the end of the text
        for char in string:
            if (char >= 'a' and char <= 'z'):
                img = imageset.imageSets["font" + char + "2"]
            elif (char >= 'A' and char <= 'Z'):
                img = imageset.imageSets["font" + char]
            elif (char == "."):
                img = imageset.imageSets["fontdot"]
            elif (char == "?"):
                img = imageset.imageSets["fontquestion"]
            elif (("font" + char) in imageset.imageSets):
                img = imageset.imageSets["font" + char]
            else:
                print ("Cannot find character: ", char)
            startX += img[0].get_width() + 1 # 1 space in-between characters
        return startX
    
    def assignText (self, go, string, color=(0, 0, 0, 255), centered = True): # if not centered, then left-aligned
        name = "TEXT" + ' '.join(map(str, color)) + string + str(centered) # save all copies of colors of strings of text
        if (name) not in imageset.imageSets:
            textSurface = pygame.Surface((self.__getLengthOfText (string), 8), pygame.SRCALPHA) # how tall is the text anyway?
            
            startX = 0 # round up or down? does it matter?

            for char in string:
                if (char >= 'a' and char <= 'z'):
                    img = imageset.imageSets ["font" + char + "2"]
                elif (char >= 'A' and char <= 'Z'):
                    img = imageset.imageSets["font" + char]
                elif (char == "."):
                    img = imageset.imageSets["fontdot"]
                elif (char == "?"):
                    img = imageset.imageSets["fontquestion"]
                elif (("font" + char) in imageset.imageSets):
                    img = imageset.imageSets["font" + char]
                else:
                    print ("char", char, "not found")

                if (color is not (0, 0, 0, 255)):
                    copy = img[0].copy() # required for custom colors....? would it be just faster to do <...>.. yeah, but eh
                    copy.fill(color, special_flags=pygame.BLEND_MAX)
                else:
                    copy = img[0]

                textSurface.blit (copy, (startX - img.origin[0] * img[0].get_width(), 0))

                startX += img[0].get_width() + 1 # uh huh
            
            imageset.imageSets [name] = imageset.ImageSet(name, self.drawingSurface)
            imageset.imageSets [name].images[0] = textSurface
            if (centered):
                self.createMesh (name, origin=[0.5,1], framesEachImage = 1)
            else:
                self.createMesh (name, origin=[0,1], framesEachImage = 1)

            print ("bleh")
        self.assignMesh (go, name)


    def setState (self, newState, *args, **kwargs):
        self.newState = newState
        self.stateChanged = True
        self.args = args
        self.kwargs = kwargs

    def endFrame(self):
        self.screen.blit (pygame.transform.scale_by(self.drawingSurface, self.scale), (0, 0)) # draw scaled drawing surface to screen buffer
        #filter
        self.screen.blit(self.gridfilter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()

        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        #dt = clock.tick(60) / 1000
        clock.tick(60) / 1000

        if (self.stateChanged):
            self.state = self.newState
            self.stateChanged = False
            # reset manager
            self.resetHandlers()
            self.onStateChange(self, self.state, self.args, self.kwargs)