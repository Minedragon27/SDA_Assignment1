import pygame
import time
from Shape import Shape
from DoBotArm import DoBotArm

class GUI:

    def __init__(self,window):
        pygame.init()
        self.__window = window
        self.__ListShapes: list[Shape]
        self.__selectedShape= None
        self.__detectedColor= 255,255,255
        self.__timerStartTime=time.time_ns()

    def addShapes(self,shapes: list[Shape]):
        self.__ListShapes=shapes
        for shape in self.__ListShapes:
            shape.drawShape(self.__window)
        
    def selectShape(self,shape: Shape,dobot: DoBotArm):
        self.__selectedShape=shape
        x,y=shape.getCenter()
        #Mapping pixels to millimeters. The X and Y are swapped due to offset in coordinate space
        RealX=(x-0)*(152 - 0) / (305 - 0) + 0  -200
        RealY=(y-0)*(152 - 0) / (320-0)+0-310

        dobot.moveArmXY(RealX,RealY,-60+shape.getDepth())

    def getShapes(self):
        return self.__ListShapes
    
    def resetTimer(self):
        self.__timerStartTime=time.time_ns()

    def checkTimer(self,targetTime: int): #targetTime in ms since the timer was reset
        if time.time_ns()-self.__timerStartTime>targetTime*1000*1000 : return True
        else: return False

    def getSelectedShape(self):
        return self.__selectedShape