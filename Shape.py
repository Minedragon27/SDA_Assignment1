
import math
import pygame

class Shape:
    def __init__(self, color, position, orientation, depth):
        self.color = color
        self.position = position  
        self.orientation = orientation  
        self.depth = depth  
        self.center = self.calculateCenter()  

    def calculateCenter(self):
        return self.position  

    def getCenter(self):
        """Returns the pre-calculated center."""
        return self.center

    def setPosition(self, position):
        self.position = position
        self.center = self.calculateCenter()  

    def getOrientation(self):
        return self.orientation

    def setOrientation(self, orientation):
        self.orientation = orientation

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def getDepth(self):
        return self.depth

    def setDepth(self, depth):
        self.depth = depth

    def getShapetype(self):
        return "shape"

    def clickedOn(self, mousePoint):
        raise NotImplementedError("Subclasses should implement this method.")

    def drawShape(self, window):
        # Placeholder for subclasses to implement specific drawing
        raise NotImplementedError("Subclasses should implement this method.")
