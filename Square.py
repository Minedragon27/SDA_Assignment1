import math
import pygame
from Shape import *

class Square(Shape):
    def __init__(self, color, position, orientation, depth, sideLength):
        super().__init__(self, color, position, orientation, depth) 
        self.__sideLength = sideLength

    def getCenter(self, orientation, sideLength):
        self.__sideLength = sideLength
        self.__orientation = orientation
        self.width = math.sin(self.__orientation)*self.__sideLength
        self.height = math.cos(self.__orientation)*self.__sideLength
        self.X = (self.width/2+self.height/2)
        self.Y = self.X
        self.center = [self.X, self.Y]
        return self.center
        
    def getShapetype(self):
        return "Square"

    def clickedOn(self, mousePoint):
        clicked = self.rect.collidepoint(mousePoint)
        return clicked

    def drawShape(self, window, sideLength):
        self.__sideLength = sideLength
        scale_Factor = 1
        square_size = self.__sideLength * scale_Factor
        square = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        square.fill(self.__color)
        pygame.draw.rect(window, self.__color, (self.__position, self.width, self.height))