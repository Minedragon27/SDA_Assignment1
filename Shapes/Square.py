import math
import pygame
from pygame.locals import *
from Shape import *

class Square(Shape):
    def __init__(self, color, position, orientation, depth, sideLength):
        super().__init__(color, position, orientation, depth) 
        self.__sideLength = sideLength
        self.__color = color  # Store color
        self.__position = position  # Initialize position
        self.__orientation = math.radians(orientation)  # Initialize orientation
        self.square_surface = None  # To hold the square surface
        self.width = math.sin(self.__orientation)*self.__sideLength + math.cos(self.__orientation)*self.__sideLength

    def getCenter(self):
        centerX = (self.width/2+self.width/2) + self.__position[0]
        centerY = - centerX + self.__position[1]
        self.center = [centerX, centerY]
        return self.center
        
    def getShapetype(self):
        return "Square"

    def drawShape(self, window: pygame.Surface):
        self.getCenter(self)
        scale_Factor = 1
        square_size = self.__sideLength * scale_Factor
        square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        square_surface.fill(self.__color)
        self.rotated_surface = pygame.transform.rotate(self.square_surface, self.__orientation)
        window.blit(self.rotated_surface, self.center)

    def clickedOn(self, mousePoint):
        if self.square_surface is None:
            return False  # Return false if the surface has not been created
        mask = pygame.mask.from_surface(self.rotated_surface)
        square_rect = self.rotated_surface.get_rect(topleft=self.center)
        relative_mouse_pos = (mousePoint[0] - square_rect.x, mousePoint[1] - square_rect.y)

        if 0 <= relative_mouse_pos[0] < square_rect.width and 0 <= relative_mouse_pos[1] < square_rect.height:
            return mask.get_at(relative_mouse_pos)  # True if clicked on the shape, False otherwise
        return False