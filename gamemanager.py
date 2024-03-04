import pygame
from gamestate import GameState

# frame rate stuff
FPS = 5

class GameManager:
    """This class represents a blank game. 

    ...

    Attributes
    ----------
    scale : int
        width/height of each pixel
    screen_pixels : tuple[int, int]
        screen's actual dimensions
    drawing_surface : pygame.Surface
        pixelated surface for gameobjects to draw themselves on
    screen : pygame.Surface
        actual screen to draw on, preceding drawing the screen filter
    current_state : str
        string description of the current gamestate the game is in
    state : GameState
        the actual current gamestate the game is in
    states : list[GameState]
        the list of possible gamestates the game can be in
    """
    def __init__(self, scale: int, pixels:tuple[int, int])->None:

        self.scale:int = scale
        self.screen_pixels:tuple[int, int] = (pixels[0]*scale, pixels[1]*scale)
        self.screen = pygame.display.set_mode(self.screen_pixels)
        self.drawing_surface = pygame.Surface (pixels)
        self.__grid_filter = self.__generate_grid_surface(scale, self.screen_pixels)
        self.__clock = pygame.time.Clock()
        self.state:GameState = None

    def __generate_grid_surface(self, scale:int, screen_pixels: tuple[int, int],
                                filter_selection:int = 2)->pygame.Surface:
        color = max(255 - (scale - 1) * 50, 0)
        alpha = min((scale - 1) * 20, 255)
        grid_color = (color, color, color, alpha)
        #SRCALPHA to make the initial image all transparent (default is all black)
        grid_filter = pygame.Surface(screen_pixels, pygame.SRCALPHA)
        if filter_selection in (1, 3):
            for x in range (0, screen_pixels[0], scale):
                pygame.draw.line(grid_filter, grid_color, (x, 0), (x, screen_pixels[1]))
            for y in range(0, screen_pixels[1], scale):
                pygame.draw.line(grid_filter, grid_color, (0, y), (screen_pixels[0], y))
            if filter_selection == 3:
                for x in range (0, screen_pixels[0] + 1, scale):
                    for y in range(0, screen_pixels[1] + 1, scale):
                        pygame.draw.polygon (grid_filter, grid_color, 
                                             [(x - 2, y),(x, y - 2), (x + 2, y), (x, y + 2)])
        if filter_selection == 2:
            grid_filter.fill(grid_color)
            for x in range (int(scale/2), screen_pixels[0], scale):
                for y in range(int(scale/2), screen_pixels[1], scale):
                    pygame.draw.circle(grid_filter, (0, 0, 0, 0), (x, y), scale/2)
        return grid_filter
    
    def __end_frame(self)->None:
        # draw scaled drawing surface to screen buffer
        self.screen.blit (pygame.transform.scale_by(self.drawing_surface, self.scale), (0, 0)) 
        # draw filter
        self.screen.blit(self.__grid_filter, (0, 0))
        # flip() the display to put your work on screen
        pygame.display.flip()

        self.__clock.tick(FPS)

        if self.state.change_state:
            self.state.change_state = False
            self.state.reset_handlers() # cleanup
            self.state = self.state.new_state

    def run(self, start:GameState)->None:
        """Starts running the game loop.

        Parameters:
            start : GameState
                The initial GameState class for the game to start with
        """
        self.state = start
        # game loop
        running = True
        while running:
            # poll for events
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if pos:
                    pos = (int(pos[0]/self.scale), int(pos[1]/self.scale))
                    self.state.handle_mouse_hover(pos)
                if event.type == pygame.QUIT:
                    self.state.reset_handlers()
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.state.handle_mouse_up(pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.handle_mouse_down(pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.state.handle_mouse_hover(pos)
                elif event.type == pygame.KEYDOWN:
                    self.state.handle_key_press(pygame.key.name(event.key))
            self.state.handle_tick()
            self.state.handle_meshes()
            self.__end_frame()
        pygame.quit()
