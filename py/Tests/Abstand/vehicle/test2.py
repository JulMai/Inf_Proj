from vehicle import Vehicle
import time
from overdrive import Overdrive

#car = Vehicle("D9:A6:FA:EB:FC:01")
#car = Vehicle("C8:1C:54:E9:9B:2C")
car = Vehicle("EC:33:B4:DB:9E:C8")
#car = Vehicle("FD:74:D8:83:05:B0")

car.changeSpeed(500, 1000)
time.sleep(1)
car.changeSpeed(0, 1000)
print(car._delegate.sum_right)
print(car._delegate.sum_left)