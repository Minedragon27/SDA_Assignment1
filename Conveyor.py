import threading
from DoBotArm import DoBotArm as dbt
import time
from serial.tools import list_ports

class Conveyor:
    def __init__(self, velocity=0, length=0, width=0, position=0,loadingPos=(200,20,0)):
        """
        Constructor to initialize the Conveyor attributes.
        :param velocity: Speed of the conveyor (int)
        :param length: Length of the conveyor (int)
        :param width: Width of the conveyor (int)
        :param position: Current position of the conveyor (int)
        """
        self.velocity = velocity
        self.length = length
        self.width = width
        self.position = position
        self.loadingPos=loadingPos
        self.EndPos=loadingPos+length-40

    def setVelocity(self,  dobot: dbt,velocity=15000):    #15000 is the max value to set the velocity at max speed
        dobot.SetConveyor(velocity!=0, speed = velocity) #with this velocity the conveyor moves with 120mm/s
        
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

    def setPosition(self, position, distance, dobot: dbt):
        
        self.setVelocity(dobot, 15000)

        self.distance = distance
        
        distance = position-self.position
        timeconstant = (120/distance)*1000
        time.sleep(timeconstant)
        dobot.SetConveyor(False, speed = 0)

        self.position = position

    def getLoadingPosition(self):
        """
        this will be a fixed position set by the dobot class
        """
        return self.loadingPos

    def goToEndPos(self, dobot: dbt):
        
        self.setPosition(self.EndPos, dobot)  #it should be reaching the end position in 5 seconds

    
        
        
