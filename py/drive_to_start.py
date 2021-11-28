from Tests.vehicle.vehicle import Vehicle
from threading import Thread
import os
import time


class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False

    
    
    def run(self):
        self.track_ids = []
        car = self._kwargs['car']
        car.setLocationChangeCallback(self.locationChangeCallback)  
          

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise


#car = Vehicle("EC:33:B4:DB:9E:C8")
car = Vehicle("D9:A6:FA:EB:FC:01")

car_l = Car_Logger(kwargs={'car': car})
car_l.start()

car.changeSpeed(600, 1000)

while(car_l.piece != 34):
    pass

car.changeSpeed(0, 1000)
time.sleep(1)
car_l.join()
del car_l
del car
os._exit(0)