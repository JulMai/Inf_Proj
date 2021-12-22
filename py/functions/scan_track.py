import time

import Car_Logger.Car_Logger_Scan as cls
from Car_Logger.Car_Logger_Scan import Car_Logger_Scan

def scan_track_with_lanes(car, speed=500):
    car_logger = cls.setup_and_start_Car_Logger(car)

    car.changeSpeed(speed, 1000)

    while (True):
        if car_logger.piece == 34 and len(car_logger.track_ids)>=4:
            break

    car.changeSpeed(0, 1000)
    time.sleep(1)

    track_t = car_logger.track_ids

    cls.stop_and_cleanup_Car_Logger(car_logger)

    return track_t