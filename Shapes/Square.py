import math
import pygame
from pygame.locals import *
from Shape import *

class Square(Shape):
    def __init__(self, color, position, orientation, depth, sideLength):
        super().__init__(color, position, orientation, depth) 
        PI = math.pi
        HALF_PI = PI / 2
        self.__sideLength = sideLength
        self.__color = color  # Store color
        self.__position = position  # Initialize position
        self.__orientation = - math.radians(orientation) + HALF_PI  # Initialize orientation
        self.square_surface = None  # To hold the square surface
        #self.width = math.sin(self.__orientation)*self.__sideLength + math.cos(self.__orientation)*self.__sideLength

    def getCenter(self):
        PI = math.pi
        HALF_PI = PI / 2
        centerX = self.__sideLength/2
        centerY = self.__sideLength/2
        cornerLength = math.sqrt(centerX ** 2 + centerY ** 2)
        cornerAngle = math.atan2(centerY, centerX)
        newAngle = cornerAngle + (self.__orientation - HALF_PI)
        self.__center = [(math.cos(newAngle) * cornerLength) + self.position[0], (-math.sin(newAngle) * cornerLength) + self.position[1]]
        return self.__center
        
    def getShapetype(self):
        return "square"

    def drawShape(self, window: pygame.Surface):
        self.getCenter()
        PI = math.pi
        HALF_PI = PI / 2
        square_surface = pygame.Surface((self.__sideLength, self.__sideLength), pygame.SRCALPHA)
        square_surface.fill(self.__color)
        self.rotated_surface = pygame.transform.rotate(square_surface, math.degrees(self.__orientation))
        rotated_rect = self.rotated_surface.get_rect(center=self.__center)
        # Blit the rotated surface onto the main window
        window.blit(self.rotated_surface, rotated_rect.topleft)
        self.rotated_rect = rotated_rect

    def clickedOn(self, mousePoint):
        if not hasattr(self, 'rotated_surface'):
            return False  # Return false if the surface hasn't been drawn yet
        # Create a mask from the rotated surface
        mask = pygame.mask.from_surface(self.rotated_surface)
        # Convert the mouse coordinates to the local coordinates of the rotated surface
        relative_mouse_pos = (mousePoint[0] - self.rotated_rect.left, mousePoint[1] - self.rotated_rect.top)
        # Check if the mouse click is within the bounds of the rotated surface
        if 0 <= relative_mouse_pos[0] < self.rotated_rect.width and 0 <= relative_mouse_pos[1] < self.rotated_rect.height:
            return mask.get_at(relative_mouse_pos)  # True if clicked on the shape, False otherwise
        return False

def test_square():
    # Pygame initialization
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("square Test")

    # Get user input for the triangle parameters
    position_input = input("Enter the centroid (x, y) as two integers (comma-separated): ")
    position = list(map(int, position_input.split(',')))

    sideLength = int(input("Enter the sidelength "))

    orientation = int(input("Enter the orientation "))

    # Create a Triangle object
    color = (0, 255, 0)  # Green color for the triangle
    depth = 0  # Depth can be 0 for now
    square = Square(color, position, orientation, depth, sideLength)
    # Test getCenter and getShapetype
    center = square.getCenter()
    shape_type = square.getShapetype()
    print(f"Center: {center}")
    print(f"Shape Type: {shape_type}")
    # Get point coordinate from user
    # Main loop
    running = True
    while running:
        window.fill((255, 255, 255))  # White background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Detect mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if square.clickedOn(mouse_pos):
                    print("square clicked!")
        # Draw the triangle on the window
        square.drawShape(window)
        # Draw the point at the specified coordinates
        pygame.draw.circle(window, (255, 0, 0), position, 5)  # Draw a red point
        pygame.draw.circle(window, (0, 0, 255), center, 5)
        # Refresh display
        pygame.display.update()
    pygame.quit()
# Call the test function
test_square()