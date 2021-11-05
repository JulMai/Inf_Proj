from overdrive import Overdrive
import time
car = Overdrive("EC:33:B4:DB:9E:C8")
car.changeSpeed(500, 1000)
time.sleep(2)
car.changeSpeed(0, 1000)
time.sleep(1)
car.changeSpeed(500, 500)
time.sleep(2)
car.changeSpeed(0, 1000)
print("finished")