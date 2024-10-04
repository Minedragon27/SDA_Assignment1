
import pygame
import time
from Shape import Shape
from DoBotArm import DoBotArm

class GUI:

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.__ListShapes=list
        self.__selectedShape= None
        self.__detectedColor= 255,255,255
        self.__timerStartTime=time.time_ns()

    def addShapes(self,shape: Shape):
        self.__ListShapes.append(shape)
        shape.drawShape(self.__screen)
        
    def selectShape(self,shape: Shape):
        DoBotArm.moveArmXYZ(shape.getPosition(),shape.getDepth())

    def getShapes(self):
        return self.__ListShapes
    def resetTimer(self):
        self.__timerStartTime=time.time_ns()
    def checkTimer(self,targetTime): #targetTime in ms since the timer was reset
        if time.time_ns()-self.__timerStartTime>targetTime*1000*1000 : return True
        else: return False