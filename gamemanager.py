from typing import Self
import pygame
from imagesdict import ImagesDict
from gameobject import GameObject
import gamestate
#from imageset import loadImages

# select from choice of filter (1-3)


# frame rate stuff
FPS = 5

class GameManager:
    """
    This class represents a blank game. 

    ...

    Attributes
    ----------
    scale : int
        width/height of each pixel
    pixels : tuple[int, int]
        screen's pixel dimensions
    screen_pixels : tuple[int, int]
        screen's actual dimensions
    drawing_surface : pygame.Surface
        surface for gameobjects to draw themselves on
    midi_out
    """
    def __init__(self, scale: int, pixels:tuple[int, int])->None:

        self.scale = scale
        self.pixels = pixels
        self.screen_pixels = (pixels[0]*scale, pixels[1]*scale)
        self.screen = pygame.display.set_mode(self.screen_pixels)
        self.drawing_surface = pygame.Surface (pixels) # surface to draw on with lower resolution than main screen. scaled when drawn onto main screen.
        self.__grid_filter = self.__generate_grid_surface(scale, self.screen_pixels)

        self.__clock = pygame.time.Clock()


        self.current_state = ""
        self.state = None
        self.states = {}

        # separate array for each object allows us to have a tonne of objects with less overhead
        # self.go_mouse_hover = []
        # self.go_mouse_down = []
        # self.go_mouse_drag = []
        # self.go_mouse_up = []
        # self.on_delete = []
        # self.on_key_press = []
        # self.on_button = []

    def __generate_grid_surface(self, scale:int, screen_pixels: tuple[int, int], filter_selection:int = 2)->pygame.Surface:
        color = max(255 - (scale - 1) * 50, 0)
        alpha = min((scale - 1) * 20, 255)
        grid_color = (color, color, color, alpha)
        grid_filter = pygame.Surface(screen_pixels, pygame.SRCALPHA) #SRCALPHA to make the initial image all transparent (default is all black)
        if (filter_selection == 1 or 3):#put into another function!!!
                for x in range (0, screen_pixels[0], scale):
                    pygame.draw.line(grid_filter, grid_color, (x, 0), (x, screen_pixels[1])) # draw black lines with 100/255 alpha
                for y in range(0, screen_pixels[1], scale):
                    pygame.draw.line(grid_filter, grid_color, (0, y), (screen_pixels[0], y))
                if (filter_selection == 3):
                    for x in range (0, screen_pixels[0] + 1, scale):
                        for y in range(0, screen_pixels[1] + 1, scale):
                            pygame.draw.polygon (grid_filter, grid_color, [(x - 2, y),(x, y - 2), (x + 2, y), (x, y + 2)])
        if (filter_selection == 2):
            grid_filter.fill(grid_color)
            for x in range (int(scale/2), screen_pixels[0], scale):
                for y in range(int(scale/2), screen_pixels[1], scale):
                    pygame.draw.circle(grid_filter, (0, 0, 0, 0), (x, y), scale/2)
        return grid_filter
    
    def add_state (self, state: gamestate)->Self:
        self.states[state.get_name()] = state
        return self
    

    def end_frame(self)->None:
        # draw scaled drawing surface to screen buffer
        self.screen.blit (pygame.transform.scale_by(self.drawing_surface, self.scale), (0, 0)) 
        # draw filter
        self.screen.blit(self.__grid_filter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        self.__clock.tick(FPS)

        if (self.state.state_changed):
            self.state.state_changed = False
            self.state.reset_handlers()
            self.current_state = self.state.new_state
            self.states[self.current_state].load_state(*self.state.args, **self.state.kwargs)
            self.state = self.states[self.current_state]



    def run(self, start)->None:
        self.current_state = start
        self.states[self.current_state].load_state()
        self.state = self.states[self.current_state]
        # game loop
        running = True
        while running:
            # poll for events
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if (pos):
                    pos = (int(pos[0]/self.scale), int(pos[1]/self.scale))
                    self.state.handle_mouse_hover(pos)
                if event.type == pygame.QUIT:
                    self.state.reset_handlers() # calls on delete for active objects if needed?
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.state.handle_mouse_up(pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.handle_mouse_down(pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.state.handle_mouse_hover(pos)
                elif event.type == pygame.KEYDOWN:
                    self.state.handle_key_press(pygame.key.name(event.key))

            if (self.current_state != ''):
                self.states[self.current_state].stateTick()
            self.state.handle_tick()
            self.state.handle_meshes()

            self.end_frame()
        pygame.quit()