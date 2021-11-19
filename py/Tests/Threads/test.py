import logging
from car import car
import time
import threading

def drive_10(car):
    car.changeSpeed(200, 1000)
    time.sleep(100)
    car.changeSpeed(0, 1000)

def check(logger):
    speed = 0
    piece = 0
    while(True):
        if logger.speed != 0:
            speed = logger.speed
            logging.info("Speed: {0}".format(logger.speed))
        if logger.piece != 0:
            piece = logger.piece
            logging.info("Piece: {0}".format(logger.piece))

        if speed != 0 or piece != 0:
            break

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

    new_car = car("EC:33:B4:DB:9E:C8")
    if new_car.car._connected: print("Car connected")
    new_car.car.changeSpeed(200, 1000)
    time.sleep(200)
    new_car.car.changeSpeed(0, 1000)
    i = new_car.logger.get_refresh_rate()
    print(i)


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