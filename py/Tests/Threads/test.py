import logging
from test_Car_Logger import Car_Logger
from car import car
import time
import threading

from overdrive import Overdrive

def drive_10(car):
    car.changeSpeed(200, 1000)
    time.sleep(100)
    car.changeSpeed(0, 1000)

def check(car):
    global logger
    logger = Car_Logger(car)
    

        


def read_lap(car, car_l):
    track_ids = []
    current_id = 33
    i = 3000
    while (True):
        if car_l.piece == 34:
            track_ids.append(34)
            car.changeSpeed(0, 1000)
            print(track_ids)
            break
        else:
            piece = car_l.piece
            if current_id != piece:
                if piece != 0:
                    track_ids.append(piece)
                    current_id = piece


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    new_car = Overdrive("EC:33:B4:DB:9E:C8")
    if new_car._connected: print("Car connected")

    log = threading.Thread(target=check, args=(new_car,))
    log.start()
    new_car.changeSpeed(200, 1000)

    time.sleep(10)

    new_car.changeSpeed(0, 1000)   
    log.join()
    
    #drive = threading.Thread(target=drive_10, args=(new_car.car,))
    #read = threading.Thread(target=read_lap, args=(new_car.car, new_car.logger))
    #drive.start()
    #print("Drive started")
    #time.sleep(2)
    #read.start()
    #print("Lap read started")

           

    
    #read.join()
    #print("Data check stopped")

    #drive.join()
    #print("Drive stopped")

    #new_car.join
    #print("Thread stopped")