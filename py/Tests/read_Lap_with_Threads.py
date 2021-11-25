import logging
from threading import Thread
import time
from track.track import Track
from Threads.test_Car_Logger import Car_Logger
from overdrive import Overdrive
from vehicle.vehicle import Vehicle


def logging_car(car):
    logging.info("Thread Logger")
    global logger
    logger = Car_Logger(car)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    #car = Overdrive("D9:A6:FA:EB:FC:01")
    car = Overdrive("EC:33:B4:DB:9E:C8")
    #car = Vehicle("EC:33:B4:DB:9E:C8")

    if car._connected:
        logging.info("Car connected")
    
    logging.info("Creating Thread for Logging")
    log = Thread(target=logging_car, args=(car,))
    logging.info("Starting Thread for Logging")
    log.start()

    time.sleep(1)

    logging.info("Accelerate Car")
    car.changeSpeed(200, 1000)
    
    track_ids = []
    current_piece = 33

    while(True):
        r_piece = logger.piece
        r_location = logger.location
        r_clockwise = logger.clockwise

        if r_piece != current_piece:
            if r_piece != 0:
                track_ids.append(r_piece)
            current_piece = r_piece
        else:
            if (r_location < last_location and r_clockwise == False) or (r_location > last_location and r_clockwise == True):
                track_ids.append(r_piece)
        if r_piece == 34:
            logging.info("Scanning Track finished")
            break
        last_location = r_location

    
    logging.info("Stopping Car")
    car.changeSpeed(0, 1000)

    logging.info("Stopping Thread for Logging")
    log.join()

    track = Track(track_ids)
    

