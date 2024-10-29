import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
from Conveyor import Conveyor

homeX, homeY, homeZ = 200, 0, 30

ctrlDobot = dbt.DoBotArm("COM7", homeX, homeY, homeZ, home= True)
conveyor=Conveyor(660,100,0)
conveyor.setVelocity(ctrlDobot,0)

print("starting")
ctrlDobot.moveHome()
ctrlDobot.moveArmXYZ(x= 200, y= 0, z= 50)
time.sleep(3)
print("moving belt")
conveyor.goToEndPos(ctrlDobot)
time.sleep(3)
ctrlDobot.moveArmRelXYZ(0,0,30)

