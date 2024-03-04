from typing import Self
from gameobject import GameObject
from imagesdict import ImagesDict

TEXT_DEBUG = False

class GameState:
    def __init__(self)->None:
        self.gos:list[GameObject] = []
        self.go_queue:list[GameObject] = []
        self.new_state:GameState = None
        self.change_state:bool = False
    #def load_state(self, *args, **wargs)->None:
    #    pass
    def stateTick(self)->None:
        pass

    def bg_color(self, color:tuple[int, int, int, int]) -> None:
        name = "bg" + ' '.join(map(str, color))
        #print (name)
        if name not in ImagesDict.images:
            bg_surface = ImagesDict.images["bgwhite"][0].copy()#pygame.Surface(ImagesDict.images["bgwhite"][0].copy().get_size())
            #print (bgSurface.get_size())
            bg_surface.fill(color)#, special_flags=pygame.BLEND_MAX)
            ImagesDict.images[name] = {}
            ImagesDict.images[name][0] = bg_surface
        self.add_game_object(GameObject()).set_image_name(name).set_pos((0, 0)).set_origin((0, 0))

    def main_ui(self, room:str)->None:
        self.add_game_object(GameObject()).set_image_name("bgwhite").set_pos((0, 0)).set_origin((0, 0))

        self.add_game_object(GameObject()).set_image_name(room).set_pos((0, 0)).set_origin((0, 0))

        self.add_game_object(GameObject()).set_image_name("bgblack").set_pos((0, 0)).set_origin((0, 0))

    def set_state (self, new_state:Self)->None:
        self.new_state = new_state
        self.change_state = True

    def add_game_object (self, go:GameObject)->GameObject:
        self.go_queue.append(go)
        return go
    def remove_game_object(self, go:GameObject)->GameObject:
        if go in self.gos:
            for function in go.on_delete:
                function()
            self.gos.remove(go)

    def handle_tick(self)->None:
        self.gos.extend(self.go_queue)
        self.go_queue.clear()
        for go in self.gos:
            self.gos.extend(go.queued_child_game_objects)
            go.queued_child_game_objects.clear()
        for go in self.gos:
            go.tick()
        for go in self.gos:
            if (go.deleted):
                self.remove_game_object(go)
    def handle_meshes(self)->None:
        for go in self.gos:
            go.draw()

    def handle_mouse_hover (self, pos:tuple[int, int]):
        for go in self.gos:
            if (len(go.on_mouse_hover) > 0):
                if (go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1]))):
                    for function in go.on_mouse_hover:
                        function()

    def handle_mouse_down (self, pos:tuple[int, int]):
        for go in self.gos:
            if (len(go.on_mouse_down) > 0):
                if (go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1]))):
                    for function in go.on_mouse_down:
                        function()

    def handle_mouse_drag (self, pos:tuple[int, int]):
        for go in self.gos:
            if (len(go.on_mouse_drag) > 0):
                if (go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1]))):
                    for function in go.on_mouse_drag:
                        function()

    def handle_mouse_up (self, pos:tuple[int, int]):
        for go in self.gos:
            if (len(go.on_mouse_up) > 0):
                if (go.contains ((pos[0] - go.get_pos()[0], pos[1] - go.get_pos()[1]))):
                    for function in go.on_mouse_up:
                        function()
                        
    def handle_key_press(self, button:str)->None:
        for go in self.gos:
            if (len(go.on_key_press) > 0):
                if (TEXT_DEBUG):
                    print ("handlekeypress:", button)
                for function in go.on_key_press:
                    function(button)
        for go in self.gos:
            if (len(go.on_button) > 0):
                for buttonname, function in go.on_button:
                    if (button == buttonname):
                        if (TEXT_DEBUG):
                            print ("handleButton:", button)
                        function()
    
    def reset_handlers (self)->None:
        for go in self.gos:
            for function in go.on_delete:
                function()
        self.gos = []