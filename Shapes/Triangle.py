import math
import pygame
from Shape import *

class Triangle(Shape):
    def __init__(self, color, topvertex, centroid, orientation, depth, sideLength): 
        super().__init__(color, centroid, orientation, depth) 
        self.__sideLength = sideLength
        self.__orientation = math.radians(orientation)
        self.__color = color
        self.__topvertex = topvertex
        self.__centroid = centroid

    def getCenter(self):
        self.__topvertex[0] - self.__centroid[0]
        angle_radians = math.atan2(self.__centroid[0] - self.__topvertex[0], self.__centroid[1] - self.__topvertex[1])
        self.__orientation = angle_radians
        perp_angle = angle_radians - 1.571
        if perp_angle >= 0 and perp_angle <= 1.571:
            topleftX = (math.cos(perp_angle) * (self.__sideLength/2)) + self.__topvertex[0]
            topleftY = (math.sin(perp_angle) * (self.__sideLength/2)) + self.__topvertex[1]
        elif perp_angle >= 1.571 and perp_angle <= 3.142:
            perp_angle = perp_angle - 1.571
            topleftX = -(math.sin(perp_angle) * (self.__sideLength/2)) + self.__topvertex[0]
            topleftY = (math.cos(perp_angle) * (self.__sideLength/2)) + self.__topvertex[1]
        elif perp_angle >= 3.142 and perp_angle <= 4.712:
            perp_angle = perp_angle - 3.142
            topleftX = -(math.cos(perp_angle) * (self.__sideLength/2)) + self.__topvertex[0]
            topleftY = -(math.sin(perp_angle) * (self.__sideLength/2)) + self.__topvertex[1]
        else:
            perp_angle = perp_angle - 4.712
            topleftX = (math.sin(perp_angle) * (self.__sideLength/2)) + self.__topvertex[0]
            topleftY = -(math.cos(perp_angle) * (self.__sideLength/2)) + self.__topvertex[1]

        centerX = self.__sideLength/2
        centerY = (2*self.__sideLength)/3
        boundHeight = math.cos(1.047)*self.__sideLength
        cornerLength = math.sqrt(centerX ** 2 + centerY ** 2)
        cornerAngle = math.atan(centerX / centerY)
        newAngle = cornerAngle - self.__orientation
        if newAngle >= 0 and newAngle <= 1.571:
            self.__center = [(math.sin(newAngle) * cornerLength) + topleftX, (-math.cos(newAngle) * cornerLength) + topleftY]
        elif newAngle >= 1.571 and newAngle <= 3.142:
            self.__center = [(math.cos(newAngle-1.571) * cornerLength) + topleftX, (math.sin(newAngle-90) * cornerLength) + topleftY]
        elif newAngle >= 3.142 and newAngle <= 4.712:
            self.__center = [(-math.sin(newAngle-3.142) * cornerLength) + topleftX, (math.cos(newAngle-180) * cornerLength) + topleftY]
        else:
            self.__center = [(-math.cos(newAngle-4.712) * cornerLength) + topleftX, (-math.sin(newAngle-270) * cornerLength) + topleftY]
        return self.__center

    def getShapetype(self):
        return "Triangle"

    def drawShape(self, window: pygame.Surface):
        center = self.getCenter()
        point1 = [center[0], center[1] + (2 * self.__sideLength) / 3]  # Bottom-left corner
        point2 = [center[0] - self.__sideLength / 2, center[1] + (self.__sideLength / 3)]  # Bottom-right corner
        point3 = [center[0] + self.__sideLength / 2, center[1] - (self.__sideLength / 3)]  # Top-middle point
        triangle_points = [point1, point2, point3]

        surface_size = self.__sideLength * 2
        triangle_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)  # Transparent surface

        # Calculate the points relative to the surface's center
        surface_center = (surface_size // 2, surface_size // 2)
        point1 = [surface_center[0], surface_center[1] + (2 * self.__sideLength) / 3]  # Bottom-left corner
        point2 = [surface_center[0] - self.__sideLength / 2, surface_center[1] + (self.__sideLength / 3)]  # Bottom-right corner
        point3 = [surface_center[0] + self.__sideLength / 2, surface_center[1] - (self.__sideLength / 3)]  # Top-middle point
        triangle_points = [point1, point2, point3]

        # Draw the triangle on the surface
        pygame.draw.polygon(triangle_surface, self.__color, triangle_points)
        rotated_surface = pygame.transform.rotate(triangle_surface, math.degrees(self.__orientation))  # Convert radians to degrees

        # Get the new rect of the rotated surface and position it to the center
        rotated_rect = rotated_surface.get_rect(center=center)

        # Blit the rotated surface onto the main window
        window.blit(rotated_surface, rotated_rect.topleft)

    def clickedOn(self, mousePoint):
        radius = (2*self.__sideLength)/(math.sqrt(3)*2)
        center = self.getCenter
        mouseX, mouseY = mousePoint
        centerX = center[0] + radius  
        centerY = center[1] + radius
        distance = math.sqrt((mouseX - centerX) ** 2 + (mouseY - centerY) ** 2)
        if distance <= radius:
            return True