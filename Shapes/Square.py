import math
import pygame
from pygame.locals import *
from Shape import Shape

# Assuming Shape is already defined elsewhere and imported
class Square(Shape):
    def __init__(self, color, position, orientation, depth, sideLength):
        super().__init__(color, position, orientation, depth)
        self.__sideLength = sideLength
        self.__color = color  # Store color
        self.__position = position  # Initialize position
        self.__orientation = orientation  # Initialize orientation
        self.square_surface = None  # To hold the square surface

    def getCenter(self, orientation, sideLength):
        self.__sideLength = sideLength
        self.__orientation = orientation
        self.width = math.sin(self.__orientation) * self.__sideLength + math.cos(self.__orientation) * self.__sideLength
        self.X = (self.width / 2)
        self.Y = self.X
        self.center = [self.X, self.Y]
        return self.center
        
    def getShapetype(self):
        return "Square"

    def drawShape(self, window: pygame.Surface):
        scale_Factor = 1
        square_size = self.__sideLength * scale_Factor
        self.square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        self.square_surface.fill(self.__color)
        self.rotated_surface = pygame.transform.rotate(self.square_surface, self.__orientation)
        window.blit(self.rotated_surface, (self.__position[0], self.__position[1]))

    def clickedOn(self, mousePoint):
        if self.square_surface is None:
            return False  # Return false if the surface has not been created
        mask = pygame.mask.from_surface(self.rotated_surface)
        square_rect = self.rotated_surface.get_rect(topleft=(self.__position[0], self.__position[1]))
        relative_mouse_pos = (mousePoint[0] - square_rect.x, mousePoint[1] - square_rect.y)

        if 0 <= relative_mouse_pos[0] < square_rect.width and 0 <= relative_mouse_pos[1] < square_rect.height:
            return mask.get_at(relative_mouse_pos)  # True if clicked on the shape, False otherwise
        return False


def test_square():
    # Pygame initialization
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Square Test")

    # Get user input for the square parameters
    centroid_input = input("Enter the centroid (x, y) as two integers (comma-separated): ")
    centroid = list(map(int, centroid_input.split(',')))

    sideLength = int(input("Enter the side length (integer): "))

    orientation = int(input("Enter the orientation of the square in degrees: "))

    # Create a Square object
    color = (255, 0, 0)  # Red color for the square
    depth = 0  # Depth can be 0 for now
    square = Square(color, centroid, orientation, depth, sideLength)

    # Test getCenter and getShapetype
    center = square.getCenter(orientation, sideLength)
    shape_type = square.getShapetype()

    print(f"Center: {center}")
    print(f"Shape Type: {shape_type}")

    # Main loop
    running = True
    while running:
        window.fill((255, 255, 255))  # White background
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            # Detect mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if square.clickedOn(mouse_pos):
                    print("Square clicked!")

        # Draw the square on the window
        square.drawShape(window)
        
        # Refresh display
        pygame.display.update()

    pygame.quit()

# Call the test function
test_square()
