import threading
from DoBotArm import DoBotArm as dbt
import time
from serial.tools import list_ports

class Conveyor:
    def __init__(self, length=700, width=100,loadingPos=0):
        """
        Constructor to initialize the Conveyor attributes.
        :param velocity: Speed of the conveyor (int)
        :param length: Length of the conveyor (int)
        :param width: Width of the conveyor (int)
        :param position: Current position of the conveyor (int)
        """
        self.velocity = 0
        self.length = length
        self.width = width
        self.position = loadingPos
        self.loadingPos=loadingPos
        self.EndPos=length-120 #only saves y coord
        

    def setVelocity(self,  dobot: dbt,velocity=15000):    #15000 is the max value to set the velocity at max speed
        
        dobot.SetConveyor(not velocity==0, velocity) #with this velocity the conveyor moves with 120mm/s
        
        self.velocity = velocity

    def getLength(self):

        #length of the conveyor is 60cm

        return self.length

    def getWidth(self):
        """
        Get the width of the conveyor.
        :return: Width of the conveyor (int)
        """
        return self.width

    def setPosition(self, position, dobot: dbt):
        
        self.setVelocity(dobot, - 15000)

        
        distance = abs(position-self.position)
        timeconstant = 2400.0/distance
        print(timeconstant)
        time.sleep(timeconstant)

        self.setVelocity(dobot,0)

        self.position = position

    def getLoadingPosition(self):
        """
        this will be a fixed position set by the dobot class
        """
        return self.loadingPos

    def goToEndPos(self, dobot: dbt):
        
        self.setPosition(self.EndPos, dobot)  #it should be reaching the end position in 5 seconds
