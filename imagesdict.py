from os import listdir
from typing import List
import pygame

# debug option
debug = False

class ImagesDict:
    images:dict[List:[pygame.Surface]] = {} # static variable
    surface:pygame.surface = None
    @staticmethod
    def __init__ (surface:pygame.Surface)->None:
        ImagesDict.surface = surface
        ImagesDict.loadResources(surface)
    @staticmethod
    def __getitem__(name:str):
        return ImagesDict.images[name]
    @staticmethod
    def drawImage (imagename:str, pos=(0, 0), origin=(0.5,0.5), frame:int=0, mirrored=False):
        if (imagename == ""):
            return
        #print ("1", imagename, frame,  len(ImagesDict.images[imagename]))
        #print ("2", frame)
        if (imagename in ImagesDict.images):
            if ("middle" in origin):
                origin2 = [0.5,0.5]
            else:
                origin2 = [-1,-1]
            if ("left" in origin):
                origin2 = [0, origin2[1]]
            elif ("right" in origin):
                origin2 = [1, origin2[1]]
            if ("top" in origin):
                origin2 = [origin2[0], 0]
            elif ("bottom" in origin):
                origin2 = [origin2[0], 1]
            if (origin2 != [-1,-1]):
                origin = origin2
            frame = frame % len(ImagesDict.images[imagename]) # automatically loop frames
            img = ImagesDict.images[imagename][frame]
            if (mirrored):
                img = pygame.transform.flip(img, True, False)
            ImagesDict.surface.blit (img, 
                                    (pos[0] - origin[0] * img.get_width(), 
                                    pos[1] - origin[1] * img.get_height())
                                    )
        else:
            print ("Erorr: imagename: [" + imagename + "." + str(frame) + "] not found!")

    # def contains (self, frame, pos):
    #     left = - self.origin[0] * self[frame].get_width() - 1
    #     top = - self.origin[1] * self[frame].get_height() - 1 
    #     right = (1 - self.origin[0]) * self[frame].get_width()
    #     bottom = (1 - self.origin[1]) * self[frame].get_height()
    #     return (pos[0] > left and pos[0] < right and pos[1] > top and pos[1] < bottom)
            
    @staticmethod
    def loadResources(surface:pygame.Surface)->None:
        files = listdir("images/") # assuming all are files
        #imageDataFile = ""
        for filename in files:
            # https://stackoverflow.com/questions/4444923/get-filename-without-extension-in-python
            splitName = filename.split (".")
            if debug:
                print (splitName)
            name = splitName[0]
            if (len(splitName) == 2):
                num = 0
                type = splitName[1]
            else:
                num = int(splitName[1])
                type = splitName[2]
            if type == "png" or type == "jpg":
                #print (name)
                if name not in ImagesDict.images:
                    #ImagesDict.images[name] = ImagesDict.images(name, surface)
                    ImagesDict.images[name] = {}
                ImagesDict.images[name] [num] = pygame.image.load("images/" + filename).convert_alpha()
            

