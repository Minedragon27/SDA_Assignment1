# importing stuff

class Shape():
    def __init__(self, color, position, orientation, depth): 
        self.__color = color
        self.__position = position
        self.__orientation = orientation
        self.__depth = depth

    def getCenter(self):
        

    def setPosition(self, position):
        self.__position = position

    def getOrientation(self):
        return self.__orientation 

    def setOrientation(self, orientation):
        self.__orientation = orientation

    def getColor(self, color):
        self.__color = color
        return self.__color

    def getDepth(self, depth):
        self.__depth = 10
        return self.__depth

    def getShapetype(self):
        return "shapeType"

    def clickedOn(self):


    def drawShape(self):
