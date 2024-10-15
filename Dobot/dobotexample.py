import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 200, 0, 30

ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= True)
print("starting")
ctrlDobot.moveHome()
time.sleep(3)
ctrlDobot.moveArmXYZ(x= 200, y= 0, z= 50)

#for i in range(1,6):
    #ctrlDobot.moveArmXYZ(x= 170, y= 0-50*i, z= 0)
#ctrlDobot.moveArmRelXY(-70,0)
ctrlDobot.moveArmXYZ(150,-255,-35)
time.sleep(3)
ctrlDobot.moveArmRelXYZ(0,0,-10)
ctrlDobot.toggleSuction()
ctrlDobot.moveArmRelXYZ(0,0,90)
time.sleep(3)
ctrlDobot.moveHome()
ctrlDobot.toggleSuction()

#ctrlDobot.moveArmRelXYZ(0,0,30)
#ctrlDobot.moveArmXYZ(x= 170, y= 60, z= -34)

#ctrlDobot.toggleSuction()
#time.sleep(1)
#ctrlDobot.moveArmRelXY(0,0,30)
#time.sleep(3)
#ctrlDobot.toggleSuction()
#ctrlDobot.moveArmXYZ(200,60,-20)
#for i in range(0,5):
    #ctrlDobot.moveArmXYZ(200-(i+1)*20,60,20)
    
#time.sleep(3)
#ctrlDobot.SetConveyor(True,-15000)
#time.sleep(3)
#ctrlDobot.SetConveyor(False,0)
#time.sleep(3)
#ctrlDobot.SetConveyor(True,15000)
#time.sleep(3)
#ctrlDobot.SetConveyor(False,0)


