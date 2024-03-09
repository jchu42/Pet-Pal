"""This module contains the static class ImagesDict to load all files on game startup for use by the game."""
from os import listdir
import traceback
import pygame
from config import Config

class ImagesDict:
    """This static class holds all of the images on the disk for use by the game.
    
    ...
    
    Attributes
    ----------
    images : dict[list:[pygame.Surface]]
        This is the dict containing all of the images, possibly animated.
        key: The name of the image or imageset in the "images/" folder
        value: A list of pygame.Surfaces with that image name. 
            If the name ends with ".#" before the ".png", it is saved to that index in the list.
    surface : pygame.Surface
        This is the surface for drawImage() to draw the images on. 
    """
    images:dict[list:[pygame.Surface]] = {} # static variable
    surface:pygame.Surface = None

    @staticmethod
    def draw_image (imagename:str, pos:tuple[int, int], origin:tuple[float, float]|str=(0.5,0.5),
                    frame:int=0, mirrored:bool=False)->None:
        """Draws the specified image to the screen.
        
        Parameters
        ----------
        imagename : str
            The name of the imageset to use
        pos : tuple[int, int]
            The position to draw the image
        origin : tuple[int, int]|str, default=(0.5, 0.5)
            The position of the image that 'pos' should be when drawn, 
            as a percentage of the image, or as a descriptive string.
            (0, 0) == "top left"
            (0.5, 0) == "top middle"
            (1, 0) == "top right"
            (0, 0.5) == "middle left"
            (0.5, 0.5) == "middle"
            (1, 0.5) == "middle right"
            (0, 1) == "bottom left"
            (0.5, 1) == "bottom middle"
            (1, 1) == "bottom right"
        frame : int, default=0
            The frame of the image to use
        mirrored : bool, default=False
            Whether or not the drawn image should be horizontally mirrored
        """
        if imagename == "":
            return
        if imagename in ImagesDict.images and imagename != '':
            if "middle" in origin:
                origin2 = [0.5,0.5]
            else:
                origin2 = [-1,-1]
            if "left" in origin:
                origin2 = [0, origin2[1]]
            elif "right" in origin:
                origin2 = [1, origin2[1]]
            if "top" in origin:
                origin2 = [origin2[0], 0]
            elif "bottom" in origin:
                origin2 = [origin2[0], 1]
            if (origin2 != [-1,-1]):
                origin = origin2
            frame = frame % len(ImagesDict.images[imagename]) # automatically loop frames
            img = ImagesDict.images[imagename][frame]
            if mirrored:
                img = pygame.transform.flip(img, True, False)
            ImagesDict.surface.blit (img,
                                    (pos[0] - origin[0] * img.get_width(),
                                    pos[1] - origin[1] * img.get_height())
                                    )
        else:
            print ("Erorr: imagename: [" + imagename + "." + str(frame) + "] not found!")
            traceback.print_exc()

    @staticmethod
    def load_resources(surface:pygame.Surface)->None:
        """Load images from the "images/" folder to the images dict.
        
        Parameters
        ----------
        surface : pygame.Surface
            The surface on which to run draw commands on"""
        debug_images = Config.config['Debug']['images'] == 'True'
        ImagesDict.surface = surface
        files = listdir("images/") # assuming all are files
        #imageDataFile = ""
        for filename in files:
            split_name = filename.split (".")
            if debug_images:
                print (split_name)
            name = split_name[0]
            if len(split_name) == 2:
                num = 0
                extension = split_name[1]
            else:
                num = int(split_name[1])
                extension = split_name[2]
            if extension in ("png", "jpg"):
                if name not in ImagesDict.images:
                    ImagesDict.images[name] = {}
                ImagesDict.images[name][num] = pygame.image.load("images/"+filename).convert_alpha()
