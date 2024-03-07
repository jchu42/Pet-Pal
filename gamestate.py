"""Contains the GameState class"""
from typing import Self
from gameobject import GameObject
from imagesdict import ImagesDict

TEXT_DEBUG = False

class GameState:
    """This class represents a state of the game. 

    ...

    Attributes
    ----------
    new_state : GameState
        The new state to switch to, if change_state is True
    change_state : bool
        When True, this state is indicating that it wants to be replaced by the next state new_state

    """
    def __init__(self)->None:
        self._gos:list[GameObject] = []
        self.__go_queue:list[GameObject] = []
        self.new_state:GameState = None
        self.change_state:bool = False


    def _state_tick(self)->None:
        """Derived classes may override this function. 
        This function is called each game tick before the GameObjects.
        """

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
        self._add_game_object(GameObject()).set_image_name(name).set_pos((30, 60))

    def _main_ui(self, room:str, border:str)->None:
        """This function creates several GameObjects to fill the background.
        
        Parameters
        ----------
        room : str
            The name of the background image to use
        """
        self._add_game_object(GameObject(imagename="bgwhite",
                                         pos=(30, 30),
                                         origin=(0.5, 0.5)))
        self._add_game_object(GameObject(imagename=room,
                                         pos=(30, 30),
                                         origin=(0.5, 0.5)))
        self._add_game_object(GameObject(imagename=border,
                                         pos=(30, 30),
                                         origin=(0.5, 0.5)))
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
        self.__go_queue.clear()

        for go in self._gos:
            go.tick()

        # run tick before adding to GameObjects, because they were created from the above go.tick(),
        # and have not had their own tick() called yet.
        for go in self._gos:
            for go2 in go.queued_child_game_objects:
                go2.tick()
            self._gos.extend(go.queued_child_game_objects)
            go.queued_child_game_objects.clear()

        # delete deleted GameObjects, and remove them from _gos list
        for go in [go for go in self._gos if go.deleted]: # wtf
            for function in go.on_delete:
                function()
        self._gos = [go for go in self._gos if not go.deleted]

    def handle_sounds(self)->None:
        """Play the queued sounds for the GameObjects"""
        for go in self._gos:
            go.play_sound()

    def handle_meshes(self)->None:
        """Draw all GameObjects to the screen."""
        for go in self._gos:
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
                if TEXT_DEBUG:
                    print ("handlekeypress:", button)
                for function in go.on_key_press:
                    function(button)
        for go in self._gos:
            if len(go.on_button) > 0:
                for buttonname, function in go.on_button:
                    if button == buttonname:
                        if TEXT_DEBUG:
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
                if TEXT_DEBUG:
                    print ("handlekeyrelease:", button)
                for function in go.on_key_release:
                    function(button)

    def reset_handlers (self)->None:
        """Handle cleanup of all GameObjects"""
        for go in self._gos:
            for function in go.on_delete:
                function()
        self._gos = []
