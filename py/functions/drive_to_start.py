from Vehicle.vehicle import Vehicle
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


def drive_to_start(car, speed=500):
    car_l = Car_Logger(kwargs={'car': car})
    car_l.start()

    car.changeSpeed(speed, 1000)

    while(car_l.piece != 34):
        pass

    car.changeSpeed(0, 1000)
    time.sleep(1)
    car_l.join()

if __name__ == '__main__':
    car = Vehicle("EC:33:B4:DB:9E:C8")
    drive_to_start(car)
    del car
    os._exit(0)