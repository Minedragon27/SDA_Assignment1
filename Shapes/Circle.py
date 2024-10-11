import math
import pygame
from Shape import Shape  # Import Shape class correctly

class Circle(Shape):
    def __init__(self, color, position, orientation, depth, radius): 
        # Initialize superclass (Shape)
        super().__init__(color, position, orientation, depth)
        self.__radius = radius
        self.__color = color
        self.__position = position

    def getCenter(self):
        """Calculate and return the center of the circle."""
        centerX = self.__position[0] + self.__radius  # Center X from the top-left position
        centerY = self.__position[1] + self.__radius  # Center Y from the top-left position
        self.center = [centerX, centerY]  # Store and return the center as a list
        return self.center

    def getShapetype(self):
        """Return the shape type."""
        return "Circle"

    def clickedOn(self, mousePoint):
        """Check if the circle was clicked by comparing the distance from the center."""
        center = self.getCenter()  # Get the center of the circle
        mouseX, mouseY = mousePoint  # Unpack the mouse click coordinates
        centerX, centerY = center  # Unpack the circle's center coordinates
        distance = math.sqrt((mouseX - centerX) ** 2 + (mouseY - centerY) ** 2)  # Calculate the distance from the center
        return distance <= self.__radius  # Return True if within the radius, False otherwise

    def drawShape(self, window: pygame.Surface):
        """Draw the circle on the provided Pygame surface."""
        center = self.getCenter()  # Get the center of the circle
        pygame.draw.circle(window, self.__color, (int(center[0]), int(center[1])), int(self.__radius))  # Draw the circle


def test_circle():
    # Pygame initialization
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Circle Test")

    # Get user input for the circle parameters
    centroid_input = input("Enter the centroid (x, y) as two integers (comma-separated): ")
    centroid = list(map(int, centroid_input.split(',')))

    radius = int(input("Enter the radius (integer): "))

    orientation = int(input("Enter the orientation of the circle in degrees (this won't affect the circle): "))

    # Create a Circle object
    color = (0, 0, 255)  # Blue color for the circle
    depth = 0  # Depth can be 0 for now
    circle = Circle(color, centroid, orientation, depth, radius)

    # Test getCenter and getShapetype
    center = circle.getCenter()
    shape_type = circle.getShapetype()

    print(f"Center: {center}")
    print(f"Shape Type: {shape_type}")

    # Main loop to display the circle
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

        # Draw the circle on the window
        circle.drawShape(window)

        # Refresh display
        pygame.display.update()

    pygame.quit()

# Call the test function
test_circle()
