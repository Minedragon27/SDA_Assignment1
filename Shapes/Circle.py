import math
import pygame
from Shape import *

class Circle(Shape):
    def __init__(self, color, position, orientation, depth, radius): 
        super().__init__(color, position, orientation, depth)
        self.__radius = radius
        self.__color = color
        self.__position = position

    def getCenter(self):
        # Calculate center based on top-left corner (self.position)
        centerX = self.__position[0] + self.__radius
        centerY = self.__position[1] - self.__radius
        self.center = [centerX, centerY]
        return self.center

    def getShapetype(self):
        return "Circle"

    def clickedOn(self, mousePoint):
        center = self.getCenter()  # Fix: Call the method
        mouseX, mouseY = mousePoint
        centerX, centerY = center
        distance = math.sqrt((mouseX - centerX) ** 2 + (mouseY - centerY) ** 2)
        if distance <= self.__radius:
            return True
        return False  # Fix: Return False if the mouse click is outside the circle

    def drawShape(self, window: pygame.Surface):
        center = self.getCenter()  # Fix: Call the method
        pygame.draw.circle(window, self.__color, (int(center[0]), int(center[1])), int(self.__radius))
