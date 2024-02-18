

class GameObject:
    def __init__(self, #imageset,
                 #onInit = lambda:False,
                 #onActivate = lambda *args, **kwargs:None,
                 #onDeactivate = lambda *args, **kwargs:None,
                 #onTick = lambda prevPos:None,
                 #onHover = lambda pos:None,
                 #onPressed = lambda pos:None,
                 #onHeld = lambda pos:None,
                 #onReleased = lambda pos:None,
                 #onCollide = lambda gameobject, corner:None):
    ):
        """
        onTick
            arguments: previous position
            return: next position of this gameobject
        """
        #self.imageset = imageset
        #self.init = onInit
        #self.active = onInit(self)
        #self.activateFunction = onActivate
        #self.deactivateFunction = onDeactivate
        #self.tickFunction = onTick
        #self.hover = onHover
        #self.pressed = onPressed
        #self.held = onHeld
        #self.released = onReleased
        
        #self.collide = onCollide

        self.active = True
        self.pos = (0, 0)
        self.nextPos = (0, 0)
        self.currentFrame = 0

    # requires it to have a mesh.. function where u don't know if the variables it uses exist is spooky
    def willChangeFrame(self):
        return self.currentFrame % self.framesEachImage == 0
    def getCurrentFrame (self):
        return int (self.currentFrame / self.framesEachImage) % len(self.images)
    def setPos (self, pos):
        self.nextPos = pos
    
    #def tick(self):
    #    #self.nextPos = self.tickFunction(self.pos)
    #    self.tickFunction(self, self.pos)
    #def draw(self):
    #    self.pos = self.nextPos
    #    self.imageset.drawImage (self.pos, self.getCurrentFrame())
    #    self.currentFrame += 1 # for next frame
    def activate(self, *args, **kwargs):
        self.currentFrame = 0
        self.active=True
        self.activateFunction(*args, **kwargs)
    def deactivate(self, *args, **kwargs):
        self.active = False
        self.deactivateFunction(*args, **kwargs)