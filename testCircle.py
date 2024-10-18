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
        centerY = self.__position[1] + self.__radius
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
        # Draw the main circle shape
        center = self.getCenter()
        pygame.draw.circle(window, self.__color, (int(center[0]), int(center[1])), int(self.__radius))
        
        # Draw the centroid (center of the circle) in red
        pygame.draw.circle(window, (255, 0, 0), (int(center[0]), int(center[1])), 5)
        
        # Draw the top-left position (position of the bounding box) in blue
        pygame.draw.circle(window, (0, 0, 255), (int(self.__position[0]), int(self.__position[1])), 5)

def test_circle():
    """Test the circle class by drawing it on a Pygame window."""
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Circle Test")

    # Get user input for the circle parameters
    position_input = input("Enter the top-left position (x, y) as two integers (comma-separated): ")
    position = list(map(int, position_input.split(',')))

    radius = int(input("Enter the radius: "))

    orientation = 0

    # Create a circle object
    color = (0, 255, 0)  # Green color for the circle
    depth = 0  # Depth can be 0 for now
    circle = Circle(color, position, orientation, depth, radius)
    
    # Test getCenter and getShapetype
    center = circle.getCenter()
    shape_type = circle.getShapetype()
    print(f"Center: {center}")
    print(f"Shape Type: {shape_type}")

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
                if circle.clickedOn(mouse_pos):
                    print("Circle clicked!")

        # Draw the circle and its markers on the window
        circle.drawShape(window)
        
        # Refresh the display
        pygame.display.update()

    pygame.quit()

# Uncomment the line below to test the circle functionality
# test_circle()
