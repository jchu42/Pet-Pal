"""This module contains the MainPet GameObject class."""
from typing import Self
import random
from gameobject import GameObject
from gameobjects.status import Status
from imagesdict import ImagesDict


class MainPet(GameObject):
    """The star of the show.

    ...

    Attributes
    ----------
    pet_type : str
        The name of the pet, determines the imageset to use
    hunger : int
        The happiness value of the pet
    action : str
        The description of the action the pet is currently performing
    poops : list[GameObject]
        The poops the pet has taken
    """
    def __init__ (self, pet_type, pet_hunger, poops, *args, **wargs)->None:
        """Initializes the MainPet with default values (subject to change)

        Parameters
        ----------
        pet_type : str
            The pet selection. Currently available: panda, cat
        """
        # pet selection?
        # idle, happyidle (default to idle if happyidle does not exist), 
        # movehori, movevert (default to movehori if does not exist)
        # eat (default to movevert, and then to movehori if does not exist)
        # dead (ends at last frame and then stays still) 
        #  (decrement self.__frame in tick to stay at last/second-last frame)

        self.pet_type = pet_type

        GameObject.__init__(self, origin=[0.5, 1], *args, **wargs)

        # self.username, self.pet_type, self.pet_happy, poop = db.get_pet(username)
        # if self.pet_type == "":
        #     raise exceptions.PetNotFoundException()

       # self.happy = pet_happy
        self.hunger = pet_hunger
        # do poop stuff

        self.set_image_name(self.pet_type + "idle")

        # self.__happy = 59
        # self.happy = 5

        self.status = Status()
        self.add_child_object(self.status)

        self._right = True
        self.action = "idle"
        self._action_value = 0
        self._change_action = True

        self.poops:list[GameObject] = []
        
        #in mainpet.py
        #set_pet(self.pet_type, self.__happy, self.poops) # test to see if its actually added to db


    def set_image_name(self, name:str|list[str])->Self:
        """Set the image set to use. 

        Parameters
        ----------
        name : str|list[str]
            str : sets the imageset to pet_type + name
            list [str] : uses pet_type + list[pos] of the lowest 'pos' value that exists

        Returns
        -------
        GameObject
            self
        """
        if isinstance(name, str):
            if not self.pet_type in name:
                name = self.pet_type + name
        else:
            for one_name in name:
                if self.pet_type + one_name in ImagesDict.images:
                    name = self.pet_type + one_name
                    break
        if name != self._image_name:
            self._image_name = name
            self._frame = 0 # reset animation state on name change
        return self

    def tick(self)->None:
        """
        change all of this when doing server things and turning it real-time

        idle, idle2, idle3...
        move, movevert (defaults to move > idle)
        sleep (defaults to idle)
        eat (defaults to movevert > move > idle)
        die (defaults to idle)
        poop (defaults to move)
        """
       # self.__happy -= 1   
        self.hunger += 1
        if self.hunger <= 0:
           # self.__happy = 59
            food = GameObject()
            food.on_mouse_up.append(lambda: setattr(self, 'hunger', self.hunger - 10))
            food.set_pos((45, 10))
            
            poop = GameObject()
            self.add_child_object(poop)
            poop.set_image_name("poop")
            poop.set_pos((int(random.random()*40 + 12), int(random.random()*40+12)))
            poop.set_frames_per_frame(3)
            poop.on_mouse_up.append(poop.set_deleted)
            self.poops.append (poop)
            if len(self.poops) > 3:
                self.poops[0].set_deleted()
                self.poops.remove(self.poops[0])
                self.hunger += 10
       # self.hunger = int(self.hunger / 10)

        if self._change_action:
            self._change_action = False
            decision = random.random() * 5
            if decision > self.hunger:
                decision = random.random() * 5
                if decision > self.hunger:
                    self.action = "sleep"
                    self._action_value = int(random.random()*30) + 30
                else:
                    self.action = "idle"
                    self._action_value = int(random.random()*15)
            else:
                if random.random() > 0.5:
                    self.action = "move"
                    self._action_value = int(random.random()*40) + 12
                else:
                    self.action = "movevert"
                    self._action_value = int(random.random()*25) + 30

        if self.action == "sleep":
            self.set_image_name(["sleep", "idle"])
            self._action_value -= 1
            if self._action_value <= 0:
                self._change_action = True
        elif self.action == "idle":
            self.set_image_name("idle")
            self._action_value -= 1
            if self._action_value <= 0:
                self._change_action = True
        elif self.action == "move":
            self.set_image_name(["move", "idle"])
            if self.get_pos()[0] < self._action_value:
                self._right = True
                self.set_pos ((self.get_pos()[0] + 1, self.get_pos()[1]))
            elif self.get_pos()[0] > self._action_value: 
                self._right = False
                self.set_pos ((self.get_pos()[0] - 1, self.get_pos()[1]))
            elif self.get_pos()[0] == self._action_value:
                self._change_action = True
        elif self.action == "movevert":
            self.set_image_name(["movevert", "move", "idle"])
            if self.get_pos()[1] < self._action_value:
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] + 1))
            elif self.get_pos()[1] > self._action_value:
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] - 1))
            elif self.get_pos()[1] == self._action_value:
                self._change_action = True

        if not self._right:
            self._mirror()

        #self.status.set_happiness(self.happy)
        self.status.set_hunger(self.hunger)
        self.status.set_pos((self.get_pos()[0], self.get_pos()[1] - 15))
