import logging
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)

from Car_Logger.Car_Logger import Car_Logger
from Vehicle.vehicle import Vehicle

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    car = Vehicle("EC:33:B4:DB:9E:C8")
    car_logger = Car_Logger(kwargs={'car': car})
    car_logger.start()
    car.changeSpeed(300, 1000)

    while car_logger.piece != 51:
        pass

    car.changeSpeed(0, 1000)
    car_logger.join()