import math
import pygame
from Shapes.Shape import Shape

class Triangle(Shape):
    def __init__(self, color, position, centroid, orientation, depth, sideLength): 
        super().__init__(color, position, orientation, depth) 
        self.__sideLength = sideLength
        self.__color = color
        self.__position = position
        self.__centroid = centroid
        angle_radians = math.atan2(self.__centroid[1] - self.__position[1], self.__centroid[0] - self.__position[0])
        self.__orientation = angle_radians

    def getCenter(self):
        #print(self.__centroid)
        PI = math.pi
        HALF_PI = PI / 2
        perp_angle = self.__orientation + HALF_PI
        topleftX = (math.cos(perp_angle) * (self.__sideLength / 2)) + self.__position[0]
        topleftY = (math.sin(perp_angle) * (self.__sideLength / 2)) + self.__position[1]
        Height = (math.sqrt(3) / 2) * self.__sideLength
        centerX = self.__sideLength/2 
        centerY = (Height/3)*2
        cornerLength = math.sqrt(centerX ** 2 + centerY ** 2)
        cornerAngle = math.atan2(centerY, centerX)
        newAngle = cornerAngle + (self.__orientation - HALF_PI)
        self.__center = [(math.cos(newAngle) * cornerLength) + topleftX, (math.sin(newAngle) * cornerLength) + topleftY]
        return self.__center

    def getShapetype(self):
        return "Triangle"

    def drawShape(self, window: pygame.Surface):
        PI = math.pi
        self.getCenter()  # Ensure the center is up-to-date
        height = (math.sqrt(3) / 2) * self.__sideLength
        center_y_offset = height / 3

        # Points relative to the centroid
        point1 = [0, -2 * center_y_offset]  # Top vertex
        point2 = [-self.__sideLength / 2, center_y_offset]  # Bottom-left vertex
        point3 = [self.__sideLength / 2, center_y_offset]  # Bottom-right vertex

        triangle_points = [point1, point2, point3]

        # Create a surface large enough to hold the triangle
        surface_size = int(self.__sideLength * 2)
        triangle_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        # Offset points to center the triangle on the surface
        triangle_points = [[x + surface_size // 2, y + surface_size // 2] for x, y in triangle_points]

        # Draw the triangle on the surface
        pygame.draw.polygon(triangle_surface, self.__color, triangle_points)

        # Rotate the surface around its center
        rotated_surface = pygame.transform.rotate(triangle_surface, -math.degrees(self.__orientation-PI/2))

        # Get the new rect of the rotated surface and position it at the centroid
        rotated_rect = rotated_surface.get_rect(center=self.__center)

        # Blit the rotated surface onto the main window
        window.blit(rotated_surface, rotated_rect.topleft)

        # Draw the centroid and position points
        pygame.draw.circle(window, (0, 0, 255), self.__center, 5)  # Centroid in blue
        pygame.draw.circle(window, (255, 0, 0), self.__position, 5)  # Position in red


    def clickedOn(self, mousePoint):
        radius = (self.__sideLength)/(math.sqrt(3))
        self.getCenter()
        mouseX, mouseY = mousePoint
        distance = math.sqrt((mouseX - self.__center[0]) ** 2 + (mouseY - self.__center[1]) ** 2)
        if distance <= radius:
            return True
        
def test_triangle():
    # Pygame initialization
    pygame.init()
    window = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Triangle Test")

    # Get user input for the triangle parameters
    position_input = input("Enter the top vertex (x, y) as two integers (comma-separated): ")
    position = list(map(int, position_input.split(',')))

    centroid_input = input("Enter the centroid (x, y) as two integers (comma-separated): ")
    centroid = list(map(int, centroid_input.split(',')))

    sideLength = (((math.sqrt((centroid[0]-position[0]) ** 2 + (centroid[1]-position[1]) ** 2))/2)*3) / 0.866

    orientation = int(0)

    # Create a Triangle object
    color = (0, 255, 0)  # Green color for the triangle
    depth = 0  # Depth can be 0 for now
    triangle = Triangle(color, position, centroid, orientation, depth, sideLength)
    # Test getCenter and getShapetype
    center = triangle.getCenter()
    shape_type = triangle.getShapetype()
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
                if triangle.clickedOn(mouse_pos):
                    print("Triangle clicked!")
        # Draw the triangle on the window
        triangle.drawShape(window)
        # Draw the point at the specified coordinates
        pygame.draw.circle(window, (0, 0, 255), centroid, 5)  # Draw a red point
        pygame.draw.circle(window, (0, 0, 255), center, 5)
        pygame.draw.circle(window, (255, 0, 0), position, 5)
        # Refresh display
        pygame.display.update()
    pygame.quit()
# Call the test function
#test_triangle()