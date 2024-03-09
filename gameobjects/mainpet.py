"""This module contains the MainPet GameObject class."""
import time
import random
from typing import Self
from gameobject import GameObject
from gameobjects.status import Status
from gameobjects.poop import Poop
from imagesdict import ImagesDict
from gamedatabase import GameDatabase as db
from config import Config

class MainPet(GameObject):
    """The star of the show.

    ...

    Attributes
    ----------
    username : str
        The user's username for use with the database
    pet_type : str
        The name of the pet, determines the imageset to use
    poops : list[Poop]
        The poops this pet owns
    last_updated : float
        The last status check of this pet
    poop_interval : int
        How often this pet should poop
    poop_max : int
        The max number of poops this pet can poop before it DIES
    hunger : int
        The happiness value of the pet
    action : str
        The description of the action the pet is currently performing
    _action_value : int
        Parameter for action
    _change_action : bool
        True when this pet's action will change
    goodbye_forever : bool
        True when this pet has taken its last breath
    """
    def __init__ (self,
                  username:str,
                  pet_type:str,
                  pet_hunger:int,
                  poops:int,
                  last_updated:float,
                  **wargs)->None:
        """Initializes the MainPet with default values (subject to change)

        Parameters
        ----------
        username : str
            The user's username
        pet_type : str
            The pet selection. Currently available: panda, cat, pig
        pet_hunger : int
            How humgwy this pet is
        poops : int
            How many poops this pet has taken
        last_updated : float
            The last unix time these stats for the pet were recorded
        """
        # pet selection?
        # idle, happyidle (default to idle if happyidle does not exist), 
        # movehori, movevert (default to movehori if does not exist)
        # eat (default to movevert, and then to movehori if does not exist)
        # dead (ends at last frame and then stays still) 
        #  (decrement self.__frame in tick to stay at last/second-last frame)
        self.username = username
        self.pet_type = pet_type

        GameObject.__init__(self, origin=[0.5, 1], **wargs)

        # self.username, self.pet_type, self.pet_happy, poop = db.get_pet(username)
        # if self.pet_type == "":
        #     raise exceptions.PetNotFoundException()

       # self.happy = pet_happy
        self.hunger = pet_hunger

        self.poops:list[Poop] = []
        for _ in range(poops):
            self._make_poop(True)
        self.last_updated = last_updated
        self.poop_interval = int(Config.config["Poop"]["interval"])
        self.poop_max = int(Config.config["Poop"]["max"])

        self.set_image_name(self.pet_type + "idle")

        #self.status = Status()
        #self.add_child_object(self.status)

        self._mirrored = True
        self.action = "idle"
        self._action_value = 0
        self._change_action = True

        self.on_delete.append(self.update_db)
        self.goodbye_forever = False

    def update_db(self)->None:
        """Update the database when game exiting"""
        db.set_pet(self.username, poops=self._get_num_poops(), last_updated=time.time())

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
        """Increment movement, resetting at end of movements
        """
        # TODO: complicated poop calculations here
        # TODO: also has to ignore sleep time somehow?
        cur_time = time.time()
        timediff = cur_time - self.last_updated
        timediff = int(timediff / self.poop_interval)
        for _ in range(timediff):
            # don't really have to update database unless exit or death
            self.last_updated = self.last_updated + self.poop_interval # retain accuracy
            if self._get_num_poops() == self.poop_max:
                self.goodbye_forever = True # trigger state change in room
            else:
                self._make_poop(False)

       # self.__happy -= 1   
        # self.hunger += 1
        # if self.hunger <= 0:
        #    # self.__happy = 59
        #     food = GameObject()
        #     food.on_mouse_up.append(lambda: setattr(self, 'hunger', self.hunger - 10))
        #     food.set_pos((45, 10))
            
        #     self._make_poop()

        #     if len(self.poops) > 3:
        #         self.poops[0].set_deleted()
        #         self.poops.remove(self.poops[0])
        #         self.hunger += 10
       # self.hunger = int(self.hunger / 10)
        self.hunger = 5 - self._get_num_poops()

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
                self._mirrored = False
                self.set_pos ((self.get_pos()[0] + 1, self.get_pos()[1]))
            elif self.get_pos()[0] > self._action_value: 
                self._mirrored = True
                self.set_pos ((self.get_pos()[0] - 1, self.get_pos()[1]))
            elif self.get_pos()[0] == self._action_value:
                self._change_action = True
        elif self.action == "movevert":
            self.set_image_name(["movevert", "jump", "move", "idle"])
            if self.get_pos()[1] < self._action_value:
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] + 1))
            elif self.get_pos()[1] > self._action_value:
                self.set_pos ((self.get_pos()[0], self.get_pos()[1] - 1))
            elif self.get_pos()[1] == self._action_value:
                self._change_action = True


        #self.status.set_happiness(self.happy)
        #self.status.set_hunger(self.hunger)
        #self.status.set_pos((self.get_pos()[0], self.get_pos()[1] - 15))

    def _get_num_poops(self)->int:
        """Get how many poops this pooper has pooped
        
        Returns
        -------
        int
            The number of poops
        """
        self.poops = list(filter(lambda poop: not poop.deleted, self.poops))
        return len(self.poops)

    def _make_poop(self, randomized:bool)->None:
        """Makes this pooper make a poop
        
        Parameters
        ----------
        randomized : bool
            True if the poop should be put in a random position on screen
            False if it should come from this pet's bum
        """
        poop = Poop()
        if randomized:
            poop.set_pos((int(random.random()*40 + 12), int(random.random()*40 + 12)))
        else:
            poop.set_pos((self.get_pos()[0] + (4 if self._mirrored else -4),
                         self.get_pos()[1]))
        self.add_child_object(poop)
        self.poops.append (poop)
        self.poops = list(filter(lambda poop: not poop.deleted, self.poops))
        