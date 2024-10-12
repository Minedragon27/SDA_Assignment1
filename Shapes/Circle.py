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
        center = self.getCenter()  # Fix: Call the method
        pygame.draw.circle(window, self.__color, (int(center[0]), int(center[1])), int(self.__radius))

def test_circle():
    """Test the circle class by drawing it on a Pygame window."""
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("circle Test")

    # Get user input for the circle parameters
    position_input = input("Enter the centroid (x, y) as two integers (comma-separated): ")
    position = list(map(int, position_input.split(',')))

    radius = int(input("Enter the side radius: "))

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
                    print("circle clicked!")

        # Draw the circle on the window
        circle.drawShape(window)
        
        # Draw the reference point at the centroid
        pygame.draw.circle(window, (255, 0, 0), position, 5)  # Draw a blue point at the centroid
        pygame.draw.circle(window, (0, 0, 255), center, 5)
        
        # Refresh the display
        pygame.display.update()

    pygame.quit()

# Call the test function
test_circle()