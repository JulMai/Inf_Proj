from threading import Lock
import time
import logging
import os
import sys



currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)

from Vehicle.vehicle import Vehicle
from functions.drive_to_start import drive_to_start
from functions.drive_to_most_left_lane import drive_to_most_left_lane
from Car_Logger.Car_Logger_Scan import scan_track
from Car_Logger.Car_Logger_distance import Car_Logger_distance
from Car_Logger.Car_Logger_distance import setup_and_start_Car_Logger as setup_and_start_Car_Logger_Dist
from functions.drive_to_most_left_lane_all_cars import drive_to_most_left_lane_all_cars

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    car1 = Vehicle("EC:33:B4:DB:9E:C8")
    logging.info("Connected to Vehicle: \"{0}\"".format(car1.addr))
    car1.abstand = 2
    car1.desired_speed = 400

    cars = {car1.addr: car1}

    drive_to_most_left_lane(car1)    
    #drive_to_start(car1)

    #logging.info("Scanning track")
    track_c = scan_track(car1)

    logging.info(str(track_c))

    time.sleep(1)

    drive_to_most_left_lane_all_cars(cars)

    #drive_to_most_left_lane(car2)
    #drive_to_most_left_lane(car3)

    lock = Lock()

    car1_logger = setup_and_start_Car_Logger_Dist(car1, cars, track_c, lock)
    logging.info("Started Threads for Car_Loggers")

    logging.info("Accel Cars")
    car1.changeSpeed(car1.desired_speed, 1000)

    time.sleep(60)

    logging.info("Stop Cars And wait")
    car1.changeSpeed(0, 1000)
    time.sleep(5)

    logging.info("Close Threads for Car_Loggers")
    car1_logger.join()
    logging.info("finished")
    os._exit(0)