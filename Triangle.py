import math
import pygame
from Shape import *

class Triangle(Shape):
    def __init__(self, color, position, orientation, depth, sideLength): 
        super().__init__(color, position, orientation, depth) 
        self.sideLength = sideLength
        self.orientation = orientation

    def getCenter(self):
        centerX = self.sideLength/2
        centerY = (2*self.sideLength)/3
        boundHeight = math.cos(60)*self.sideLength
        cornerLength = math.sqrt(centerX ** 2 + centerY ** 2)
        cornerAngle = math.atan(centerX / centerY)
        newAngle = cornerAngle - self.orientation
        if newAngle >= 0 & newAngle <= 90:
            self.center = (math.sin(newAngle) * cornerLength, math.cos(newAngle) * cornerLength)
        elif newAngle >= 90 & newAngle <= 180:
            self.center = (math.cos(newAngle-90) * cornerLength, -math.sin(newAngle-90) * cornerLength)
        elif newAngle >= 180 & newAngle <= 270:
            self.center = (math.sin(newAngle-180) * cornerLength, math.cos(newAngle-180) * cornerLength)
        else:
            self.center = (math.sin(newAngle-270) * cornerLength, math.cos(newAngle-270) * cornerLength)
    def getShapetype(self):
        return "Triangle"

    def clickedOn(self, mousePoint):


    def drawShape(self):
