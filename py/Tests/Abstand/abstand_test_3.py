from threading import Thread
import time
import logging
import os


from Vehicle.vehicle import Vehicle




if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    car1 = Vehicle("D9:A6:FA:EB:FC:01")
    #car1 = Vehicle("C8:1C:54:E9:9B:2C")
    logging.info("Connected to Vehicle: \"{0}\"".format(car1.addr))
    car1.abstand = 1
    car1.desired_speed = 500

    car2 = Vehicle("EC:33:B4:DB:9E:C8")
    logging.info("Connected to Vehicle: \"{0}\"".format(car2.addr))
    car2.abstand = 2
    car2.desired_speed = 400

    car3 = Vehicle("C8:1C:54:E9:9B:2C")
    logging.info("Connected to Vehicle: \"{0}\"".format(car3.addr))
    car3.abstand = 3
    car3.desired_speed = 350

    cars = {car1.addr: car1, car2.addr: car2, car3.addr: car3}

    drive_to_start(car1)

    logging.info("Scanning track")
    track_t = scan_track_with_lanes(car1)

    #track = get_track_with_lanes(track_t)

    #track_c = get_track_dict(track_t)

    track_c = track_to_dict(track_t)

    logging.info(str(track_c))

    time.sleep(1)

    car1_logger = Car_Logger(kwargs={'car': car1})
    car2_logger = Car_Logger(kwargs={'car': car2})
    car3_logger = Car_Logger(kwargs={'car': car3})
    car1_logger.start()
    car2_logger.start()
    car3_logger.start()
    logging.info("Started Threads for Car_Loggers")

    logging.info("Accel Cars")
    car1.changeSpeed(car1.desired_speed, 1000)
    car2.changeSpeed(car2.desired_speed, 1000)
    car3.changeSpeed(car3.desired_speed, 1000)

    time.sleep(600)

    logging.info("Stop Cars And wait")
    car1.changeSpeed(0, 1000)
    time.sleep(1)
    car2.changeSpeed(0, 1000)
    time.sleep(5)

    logging.info("Close Threads for Car_Loggers")
    car1_logger.join()
    car2_logger.join()
    car3_logger.join()
    logging.info("finished")
    os._exit(0)
