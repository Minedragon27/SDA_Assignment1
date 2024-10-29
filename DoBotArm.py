
#!/usr/bin/env python

import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType
import time


"""-------The DoBot Control Class-------
Variables:
suction = Suction is currently on/off
picking: shows if the dobot is currently picking or dropping an item
api = variable for accessing the dobot .dll functions
home% = home position for %
                                  """
####### List of future possibilities ######
## Joint angles
## Speed vs Accell modes?
##SetPTPCoordinateParams(api, xyzVelocity, xyzAcceleration, rVelocity,  rAcceleration,  isQueued=0):
## Other misc features from the dType and/or the DoBot studio

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

#Main control class for the DoBot Magician.
class DoBotArm:
    def __init__(self, port, homeX, homeY, homeZ, home = False, homingWait = True):
        self.suction = False
        self.picking = False
        self.api = dType.load()
        self.port = port
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.rotation = 0
        self.connected = False
        self.home_time = 0
        self.dobotConnect(home, homingWait)
        self.lastIndex = 0
        self.rotation = self.getPosition()[3]

    def __del__(self):
        self.dobotDisconnect()

    #Attempts to connect to the dobot
    def dobotConnect(self, home = True, homingWait = True):
        if(self.connected):
            print("You're already connected")
        else:
            state = dType.ConnectDobot(self.api, self.port, 115200)[0]
            if(state == dType.DobotConnect.DobotConnect_NoError):
                print("Connect status:",CON_STR[state])
                # If homingWait is set to false, wait_rehoming needs to be called before executing Dobot commands
                # Useful when some initilisation needs to be done
                if(home):
                    self.rehome(None, None, None, homingWait)
                self.connected = True
                return self.connected
            else:
                print("Unable to connect")
                print("Connect status:",CON_STR[state])
                return self.connected

    def rehome(self, x, y, z, wait = True):
        if(x != None):
            self.homeX = x
        if(y != None):
            self.homeY = y
        if(z != None):
            self.homeZ = z
        dType.SetQueuedCmdClear(self.api)

        dType.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued = 1)
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

        self.lastIndex = dType.SetHOMECmd(self.api, temp = 0, isQueued = 1)
        self.home_time = time.time()
        if(wait):
            time.sleep(25)
        
    def wait_rehoming(self):
        if(self.home_time > (time.time() - 25)):
            time.sleep(25 + self.home_time - time.time())
        

    #Returns to home location and then disconnects
    def dobotDisconnect(self):
        self.moveHome()
        dType.DisconnectDobot(self.api)

    #Delays commands
    def commandDelay(self, lastIndex = None):
        if(lastIndex == None):
            lastIndex = self.lastIndex
        dType.SetQueuedCmdStartExec(self.api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(200)
        dType.SetQueuedCmdStopExec(self.api)

    #Toggles suction peripheral on/off
    def toggleSuction(self, wait = True):
        lastIndex = 0
        if(self.suction):
            self.lastIndex = dType.SetEndEffectorSuctionCup( self.api, True, False, isQueued = 0)[0]
            self.suction = False
        else:
            self.lastIndex = dType.SetEndEffectorSuctionCup(self.api, True, True, isQueued = 0)[0]
            self.suction = True
        if(wait):
            self.commandDelay(self.lastIndex)
        return self.lastIndex

    def getPosition(self):
        return dType.GetPose(self.api)

    def moveArmRelXY(self, xrel, yrel, wait = True, jump = False):
        positions = self.getPosition()
        return self.moveArmXY(positions[0] + xrel, positions[1] + yrel, wait, jump)

    #Moves arm to X/Y/Z Location
    def moveArmXY(self,x,y, wait = True, jump = False):
        return self.moveArmXYZ(x, y, self.homeZ, wait, jump)
    
    def moveArmRelXYZ(self, xrel, yrel, zrel, wait = True, jump = False):
        positions = self.getPosition()
        return self.moveArmXYZ(positions[0] + xrel, positions[1] + yrel, positions[2] + zrel, wait, jump)
    
    
    # By passing on None as a coordinate parameter, the current arm position in givven axis will be used
    def moveArmXYZ(self,x,y, z, wait = True, jump = False):
        if(x == None or y == None or z == None):
            position = self.getPosition()
            if(x == None):
                x = position[0]
            if(y == None):
                y = position[1]
            if(z == None):
                z = position[2]
        mode = dType.PTPMode.PTPJUMPXYZMode if jump else dType.PTPMode.PTPMOVLXYZMode
        self.lastIndex = dType.SetPTPCmd(self.api, mode, x, y, z, self.rotation)[0]
        if(wait):
            self.commandDelay(self.lastIndex)
        return self.lastIndex

    def SetConveyor(self, enabled, speed = 15000):
        self.lastIndex = dType.SetEMotor(self.api, 0, enabled, speed, isQueued = 1)[0]
        self.commandDelay(self.lastIndex)
        
    def RotateHead(self, rotation, wait = True):
        self.rotation = rotation
        self.moveArmRelXYZ(0, 0, 0, wait)

    #Returns to home location
    def moveHome(self, wait = True):
        self.lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, self.homeX, self.homeY, self.homeZ, self.rotation)[0]
        if(wait):
            self.commandDelay(self.lastIndex)
        return self.lastIndex

    #Toggles between hover and item level
    def pickToggle(self, itemHeight, wait = True):
        lastIndex = 0
        positions = self.getPosition()
        if(self.picking):
            self.moveArmXYZ(None, None, self.homeZ, wait)
            self.picking = False
        else:
            self.moveArmXYZ(None, None, itemHeight, wait)
            self.picking = True
        #if(wait):
        #    self.commandDelay(self.lastIndex)
        return self.lastIndex
