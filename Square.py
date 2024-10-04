import math
import pygame
from pygame.locals import *
from Shape import *

class Square(Shape):
    def __init__(self, color, position, orientation, depth, sideLength):
        super().__init__(self, color, position, orientation, depth) 
        self.__sideLength = sideLength

    def getCenter(self, orientation, sideLength):
        self.__sideLength = sideLength
        self.__orientation = orientation
        self.width = math.sin(self.__orientation)*self.__sideLength + math.cos(self.__orientation)*self.__sideLength
        self.X = (self.width/2+self.width/2)
        self.Y = self.X
        self.center = [self.X, self.Y]
        self.rect = pygame.Rect(self.X-(self.width/2), self.Y+(self.width/2), self.__sideLength ,self.__sideLength)
        return self.center
        
    def getShapetype(self):
        return "Square"

    def drawShape(self, window: pygame.display, sideLength, orientation, position):
        self.__sideLength = sideLength
        self.__orientation = orientation
        self.__position = position
        scale_Factor = 1
        square_size = self.__sideLength * scale_Factor
        square = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        square.fill(self.__color)
        rotated_surface = pygame.transform.rotate(square, orientation)
        window.blit(rotated_surface, square)

    def clickedOn(self, mousePoint):
        mask = pygame.mask.from_surface(square)
        clicked = self.rect.collidepoint(mousePoint)
        return clicked