from vehicle import Vehicle
from threading import Thread
import logging
import time




class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    c_locations = {}
    
    def run(self):
        self.track_ids = []
        car = self._kwargs['car']
        car.setLocationChangeCallback(self.locationChangeCallback)  
          

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):        
        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise

        if piece == 10:
            if not location in self.c_locations:
                logging.info("location: {0}".format(location))
                self.c_locations[location] = ""
            else:
                time.sleep(0.5)
                car.changeLaneLeft(speed, 1000)



format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

car = Vehicle("EC:33:B4:DB:9E:C8")
#car = Vehicle("D9:A6:FA:EB:FC:01")

car_logger = Car_Logger(kwargs={'car': car})
car_logger.start()

car.changeSpeed(500, 1000)

time.sleep(1000)

car.changeSpeed(0, 1000)

car_logger.join()

