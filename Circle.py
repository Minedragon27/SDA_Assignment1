import math
import pygame

class Circle(Shape):
    def __init__(self, color, position, orientation, depth, radius): 
        self.radius = radius

    def getCenter(self):
        self.center = [-self.radius/2, self.radius/2]

    def getShapetype(self):
        return "Circle"

    def clickedOn(self, mousePoint):
        mouseX, mouseY = mousePoint
        centerX = self.x + self.radius  
        centerY = self.y + self.radius
        distance = math.sqrt((mouseX - centerX) ** 2 + (mouseY - centerY) ** 2)
        if distance <= self.radius:
            return True

    def drawShape(self):
        pygame.draw.circle(self.window, self.color, (int(self.x + self.radius), int(self.y + self.radius)), int(self.radius))