from gameobject import GameObject
from gameobjects.status import Status
from typing import Self
from imagesdict import ImagesDict
import random
import gamemanager

class MainPet(GameObject):
    def __init__ (self, pet_type:str)->None:
        # pet selection?
        # idle, happyidle (default to idle if happyidle does not exist), 
        # movehori, movevert (default to movehori if does not exist)
        # eat (default to movevert, and then to movehori if does not exist)
        # dead (ends at last frame and then stays still) (decrement self.__frame in tick to stay at last/second-last frame)

        GameObject.__init__(self, [0.5, 1])

        self.pet_type = pet_type
        self.set_image_name(self.pet_type + "idle")

        self.__happy = 59
        self.happy = 5

        self.add_child_object(Status(self))

        self.right = True
        self.action = "idle"
        self.action_value = 0
        self.change_action = True

        self.poops:list[GameObject] = []

    def set_image_name(self, name:str|list[str])->Self:
        if (isinstance(name, str)):
            if (not self.pet_type in name):
                name = self.pet_type + name
        else:
            for one_name in name:
                if ((self.pet_type + one_name) in ImagesDict.images):
                    name = self.pet_type + one_name
                    break
        if (name != self._image_name):
            self._image_name = name
            self._frame = 0 # reset animation state on name change
        return self
    
    def tick(self)->None:
        self.__happy -= 1 # change happiness and stuff when doing server things and turning it real-time
        if (self.__happy < 0):
            self.__happy = 59

            poop = GameObject()
            self.add_child_object(poop)
            poop.set_image_name("poop")
            poop.set_pos((int(random.random()*40 + 10), int(random.random()*40+10)))
            poop.set_frames_per_frame(3)
            poop.on_mouse_up.append(poop.set_deleted())
            self.poops.append (poop)
            if (len(self.poops) > 3):
                self.poops[0].deleteSelf()
                self.poops.remove(self.poops[0])
        self.happy = int(self.__happy / 10)

        # idle, idle2, idle3...
        # move, movevert (defaults to move > idle)
        # sleep (defaults to idle)
        # eat (defaults to movevert > move > idle)
        # die (defaults to idle)
        # poop (defaults to move)
        if self.change_action:
            self.change_action = False
            decision = random.random() * 5
            if (decision > self.happy):
                decision = random.random() * 5
                if (decision > self.happy):
                    self.action = "sleep"
                    self.action_value = int(random.random()*30) + 30
                else:
                    self.action = "idle"
                    self.action_value = int(random.random()*15)
            else:
                if (random.random() > 0.5):
                    self.action = "move"
                    self.action_value = int(random.random()*40) + 10
                else:
                    self.action = "movevert"
                    self.action_value = int(random.random()*25) + 30
        
        if (self.action == "sleep"):
            self.set_image_name(["sleep", "idle"])
            self.action_value -= 1
            if (self.action_value <= 0):
                self.change_action = True
        elif (self.action == "idle"):
            self.set_image_name("idle")
            self.action_value -= 1
            if (self.action_value <= 0):
                self.change_action = True
        elif (self.action == "move"):
            self.set_image_name(["move", "idle"])
            if (self.get_pos()[0] < self.action_value):
                self.right = True
                self.set_pos ((self.get_pos()[0] + 1, self.get_pos()[1]))
            elif (self.get_pos()[0] > self.action_value): 
                self.right = False
                self.set_pos ((self.get_pos()[0] - 1, self.get_pos()[1]))
            elif (self.get_pos()[0] == self.action_value):
                self.change_action = True
        elif (self.action == "movevert"):
            self.set_image_name(["movevert", "move", "idle"])
            if (self.get_pos()[1] < self.action_value):
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] + 1))
            elif (self.get_pos()[1] > self.action_value):
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] - 1))
            elif (self.get_pos()[1] == self.action_value):
                self.change_action = True

        if (not self.right):
            self.mirror()
