from vehicle.vehicle import Vehicle
import time
import os

car = Vehicle("D9:A6:FA:EB:FC:01")

i = 0
last_status = 0

while(True):
    car.sendBatteryStatusRequest()
    time.sleep(1)
    if last_status != car.getBatteryStatus():
        last_status = car.getBatteryStatus()
        print(car.getBatteryStatus())
   
    i += 1
    if i > 100:
        break

os._exit(0)
