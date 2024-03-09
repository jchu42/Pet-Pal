"""Contains the GameState class"""
from typing import Self
import pygame
from gameobject import GameObject
from imagesdict import ImagesDict
from config import Config

class GameState:
    """This class represents a state of the game. 

    ...

    Attributes
    ----------
    _gos : list[GameObject], default=[]
        The list of GameObjects in this GameState. 
    _gos_draw_order : dict[list[GameObject]] = {}
        The same list of GameObjects in this GameState put in a dictionary
        in order to draw them in the correct layer order
    __go_queue : list[GameObject] = []
        The list of GameObjects that are queued to be added to the main lists.
        This is required to prevent events from triggering on newly created GameObjects.
        When a GameObject triggers additions to a GameState's GameObjects, 
            they must be added *after* the event actions are all triggered, 
            or else they themselves will also trigger on the same action event queue items.
    new_state : GameState
        The new state to switch to, if change_state is True
    change_state : bool
        When True, this state is indicating that it wants to be replaced by the next state new_state
    _text_debug : bool
        Read from config file; True to show key presses
    music : pygame.mixer.music
        The thing that controls music playback
    music_button : GameObject
        The toggle music buttpm
    """
    def __init__(self)->None:
        """Initialize the GameState to a safe empty state."""
        self._gos:list[GameObject] = []
        self._gos_draw_order:dict[list[GameObject]] = {}
        self.__go_queue:list[GameObject] = []
        self.new_state:GameState = None
        self.change_state:bool = False
        self._text_debug = Config.config['Debug']['text'] == 'True'
        #self._add_game_object(GameObject()).queue_sound(63) # play a sound when going to next state

        self.music = pygame.mixer.music
        self.music_button = self._add_game_object(GameObject(pos=(60, 60),
                                                             imagename="musicon" if self.music.get_busy() else "musicoff",
                                                             origin=(1, 1),
                                                             layer=11,
                                                             on_mouse_up=[self.set_music_button]))

    def set_music_button (self):
        """Toggles music and button"""
        if not self.music.get_busy():
            self.music_button.set_image_name("musicon")
            self.music.play(-1)
        else:
            self.music_button.set_image_name("musicoff")
            self.music.stop()

    def _state_tick(self)->None:
        """Derived classes may override this function. 
        This function is called each game tick before the GameObjects.
        """
        pass

    def _bg_color(self, color:tuple[int, int, int, int]) -> None:
        """This function creates a GameObject to fill the background with the given color.
        
        Parameters
        ----------
        color : tuple[int, int, int, int]
            The color to set the whole screen to
        """
        name = "bg" + ' '.join(map(str, color))
        if name not in ImagesDict.images:
            bg_surface = ImagesDict.images["bgwhite"][0].copy()
            bg_surface.fill(color)
            ImagesDict.images[name] = {}
            ImagesDict.images[name][0] = bg_surface
        self._add_game_object(GameObject(imagename=name,
                                         pos=(30, 60),
                                         layer=-1))

    def _main_ui(self, room:str, border:str)->None:
        """This function creates several GameObjects to fill the background.
        
        Parameters
        ----------
        room : str
            The name of the background image to use
        border : str
            The name of the border image to use
        """
        self._add_game_object(GameObject(imagename="bgwhite",
                                         pos=(30, 30),
                                         origin=(0.5, 0.5),
                                         layer=-2))
        self._add_game_object(GameObject(imagename=room,
                                         pos=(30, 30),
                                         origin=(0.5, 0.5),
                                         layer=-1))
        self._add_game_object(GameObject(imagename=border,
                                         pos=(30, 30),
                                         origin=(0.5, 0.5),
                                         layer=10))
        #self._add_game_object(GameObject()).set_image_name("bgblack2").set_pos((30, 70))

    def _set_state (self, new_state:Self)->None:
        """Call this function to exit the current state and transition to the new state.
        
        Parameters
        ----------
        new_state : GameState
            The new state to transition to
        """
        self.new_state = new_state
        self.change_state = True

    def _add_game_object (self, go:GameObject)->GameObject:
        """Add a GameObject to the game state, so it will be used and appear on the screen.
        
        Parameters
        ----------
        go : GameObject
            The GameObject to add to the current state
        
        Returns
        -------
        GameObject
            The GameObject that was added
        """
        self.__go_queue.append(go)
        return go

    def handle_tick(self)->None:
        """Game and GameObject logic."""
        self._state_tick()

        self._gos.extend(self.__go_queue)
        for go in self.__go_queue:
            if go.layer not in self._gos_draw_order:
                self._gos_draw_order[go.layer] = []
            self._gos_draw_order[go.layer].append(go)
        self.__go_queue.clear()

        for go in self._gos:
            go.tick()

        # run tick before adding to GameObjects, because they were created from the above go.tick(),
        # and have not had their own tick() called yet.
        for go in self._gos:
            for go2 in go.queued_child_game_objects:
                go2.tick()

                if go2.layer not in self._gos_draw_order:
                    self._gos_draw_order[go2.layer] = []
                self._gos_draw_order[go2.layer].append(go2)

            self._gos.extend(go.queued_child_game_objects)
            go.queued_child_game_objects.clear()

        # delete deleted GameObjects, and remove them from _gos list
        for go in [go for go in self._gos if go.deleted]: # wtf
            for function in go.on_delete:
                function()
        self._gos = [go for go in self._gos if not go.deleted]
        for key in self._gos_draw_order.keys():
            self._gos_draw_order[key] = [go for go in self._gos_draw_order[key] if not go.deleted]

    def handle_sounds(self)->None:
        """Play the queued sounds for the GameObjects"""
        for go in self._gos:
            go.play_sound()

    def handle_meshes(self)->None:
        """Draw all GameObjects to the screen."""
        for _, layer in sorted(self._gos_draw_order.items()):
            for go in layer:
                go.draw()

    def handle_mouse_hover (self, pos:tuple[int, int])->None:
        """Handle all GameObjects' mouse hover actions if the cursor is over it
        
        Parameters
        ----------
        pos : tuple[int, int]
            The position of the mouse
        """
        for go in self._gos:
            if len(go.on_mouse_hover) > 0:
                if go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1])):
                    for function in go.on_mouse_hover:
                        function()

    def handle_mouse_down (self, pos:tuple[int, int])->None:
        """Handle all GameObjects' mouse down actions if the cursor is over it
        
        Parameters
        ----------
        pos : tuple[int, int]
            The position of the mouse
        """
        for go in self._gos:
            if len(go.on_mouse_down) > 0:
                if go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1])):
                    for function in go.on_mouse_down:
                        function()

    def handle_mouse_drag (self, pos:tuple[int, int])->None:
        """Handle all GameObjects' mouse drag actions if the cursor is over it
        
        Parameters
        ----------
        pos : tuple[int, int]
            The position of the mouse
        """
        for go in self._gos:
            if len(go.on_mouse_drag) > 0:
                if go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1])):
                    for function in go.on_mouse_drag:
                        function()

    def handle_mouse_up (self, pos:tuple[int, int])->None:
        """Handle all GameObjects' mouse up actions if the cursor is over it
        
        Parameters
        ----------
        pos : tuple[int, int]
            The position of the mouse
        """
        for go in self._gos:
            if len(go.on_mouse_up) > 0:
                if go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1])):
                    for function in go.on_mouse_up:
                        function()

    def handle_key_press(self, button:str)->None:
        """Handle all GameObjects' keyboard actions
        
        Parameters
        ----------
        button : str
            The key that was pressed
        """
        for go in self._gos:
            if len(go.on_key_press) > 0:
                if self._text_debug:
                    print ("handlekeypress:", button)
                for function in go.on_key_press:
                    function(button)
        for go in self._gos:
            if len(go.on_button) > 0:
                for buttonname, function in go.on_button:
                    if button == buttonname:
                        if self._text_debug:
                            print ("handleButton:", button)
                        function()

    def handle_key_release(self, button:str)->None:
        """Handle all GameObjects' keyboard actions
        
        Parameters
        ----------
        button : str
            The key that was pressed
        """
        for go in self._gos:
            if len(go.on_key_release) > 0:
                if self._text_debug:
                    print ("handlekeyrelease:", button)
                for function in go.on_key_release:
                    function(button)

    def reset_handlers (self)->None:
        """Handle cleanup of all GameObjects"""
        for go in self._gos:
            for function in go.on_delete:
                function()
        self._gos = []
        self._gos_draw_order = {}
