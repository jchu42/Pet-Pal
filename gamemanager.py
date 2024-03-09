"""Contains the GameManager class that represents a blank game"""
import pygame
from gamestate import GameState
from config import Config

class GameManager:
    """This class represents a blank game. 

    ...

    Attributes
    ----------
    __fps : int
        The FPS to run the game at
    __scale : int
        Width/height of each pixel
    __screen_pixels : tuple[int, int]
        Screen's actual dimensions
    __screen : pygame.Surface
        Actual screen to draw on, preceding drawing the screen filter
    drawing_surface : pygame.Surface
        Pixelated surface for gameobjects to draw themselves on
    __grid_filter : pygame.Surface
        The screen filter to put on top of the scaled pixel image
    __clock : pygame.time.Clock
        Used to llmit the frame rate
    state : GameState
        The actual current gamestate the game is in
    """
    def __init__(self, fps: int, scale: int, pixels:tuple[int, int])->None:
        """Initializes the GameManager, setting up the screen and clock
        
        Parameters
        ----------
        fps : int
            The FPS to run the game at
        scale : int
            The size of the pixels to be drawn
        pixels : tuple[int, int]
            The screen pixel dimensions. Multiplied by scale for actual screen size.
        """
        self.__fps = fps
        self.__scale:int = scale
        self.__screen_pixels:tuple[int, int] = (pixels[0]*scale, pixels[1]*scale)
        self.__screen = pygame.display.set_mode(self.__screen_pixels)
        self.drawing_surface = pygame.Surface (pixels)
        self.__grid_filter = self.__generate_grid_surface()
        self.__clock = pygame.time.Clock()
        self.__state:GameState = None

    def __generate_grid_surface(self)->pygame.Surface:
        """Create the screen filter to give the game a retro look
        
        Returns
        -------
        pygame.Surface
            The screen filter with the screen's dimensions
        """
        color = max(255 - (self.__scale - 1) * 50, 0)
        alpha = min((self.__scale - 1) * 20, 255)
        grid_color = (color, color, color, alpha)
        #SRCALPHA to make the initial image all transparent (default is all black)
        grid_filter = pygame.Surface(self.__screen_pixels, pygame.SRCALPHA)
        filter_selection = int(Config.config['Screen']['filter'])
        if filter_selection in (1, 3):
            for x in range (0, self.__screen_pixels[0], self.__scale):
                pygame.draw.line(grid_filter, grid_color, (x, 0), (x, self.__screen_pixels[1]))
            for y in range(0, self.__screen_pixels[1], self.__scale):
                pygame.draw.line(grid_filter, grid_color, (0, y), (self.__screen_pixels[0], y))
            if filter_selection == 3:
                for x in range (0, self.__screen_pixels[0] + 1, self.__scale):
                    for y in range(0, self.__screen_pixels[1] + 1, self.__scale):
                        pygame.draw.polygon (grid_filter, grid_color, 
                                             [(x - 2, y),(x, y - 2), (x + 2, y), (x, y + 2)])
        if filter_selection == 2:
            grid_filter.fill(grid_color)
            for x in range (int(self.__scale/2), self.__screen_pixels[0], self.__scale):
                for y in range(int(self.__scale/2), self.__screen_pixels[1], self.__scale):
                    pygame.draw.circle(grid_filter, (0, 0, 0, 0), (x, y), self.__scale/2)
        return grid_filter

    def __end_frame(self)->bool:
        """Draw the pixel screen to the actual screen, tick clock, and manage state changes
        
        Returns
        -------
        bool
            True if the game should continue running
        """
        # draw scaled drawing surface to screen buffer
        self.__screen.blit (pygame.transform.scale_by(self.drawing_surface, self.__scale), (0, 0)) 
        # draw filter
        self.__screen.blit(self.__grid_filter, (0, 0))
        # flip() the display to put work on screen
        pygame.display.flip()

        self.__clock.tick(self.__fps)

        if self.__state.change_state:
            self.__state.change_state = False
            self.__state.reset_handlers() # cleanup
            self.__state = self.__state.new_state
            if self.__state is None:
                return False
        return True

    def run(self, start:GameState)->None:
        """Starts running the game loop.

        Parameters
        ----------
        start : GameState
            The initial GameState class for the game to start with
        """
        self.__state = start

        running = True
        while running:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if pos:
                    pos = (int(pos[0]/self.__scale), int(pos[1]/self.__scale))
                    self.__state.handle_mouse_hover(pos)
                if event.type == pygame.QUIT:
                    self.__state.reset_handlers()
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__state.handle_mouse_up(pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__state.handle_mouse_down(pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.__state.handle_mouse_hover(pos)
                elif event.type == pygame.KEYDOWN:
                    self.__state.handle_key_press(pygame.key.name(event.key))
                elif event.type == pygame.KEYUP:
                    self.__state.handle_key_release(pygame.key.name(event.key))
            self.__state.handle_tick()
            self.__state.handle_sounds()
            self.__state.handle_meshes()
            if not self.__end_frame():
                running = False
        pygame.quit()
