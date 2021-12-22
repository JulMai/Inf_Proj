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

    expected_track = [33, 10, 18, 17, 20, 10, 17, 48, 18, 18, 34]
    speeds = [300, 350, 400, 450, 500, 600]
    tests = []
    test_log = ""


    car = Vehicle("D9:A6:FA:EB:FC:01")
    #car = Overdrive("EC:33:B4:DB:9E:C8")
    #car = Vehicle("EC:33:B4:DB:9E:C8")

    if car._connected:
        logging.info("Car connected")
    
    i = 0

    for speed in speeds:
        i = i + 1
        logging.info("Start Test {0}: Speed: {1}".format(str(i), str(speed)))
        test_log = test_log + "Start Test {0}: Speed: {1} \n".format(str(i), str(speed))
        
        #logging.info("Creating Thread for Logging")
        log = Thread(target=logging_car, args=(car,))
        #logging.info("Starting Thread for Logging")
        log.start()

        time.sleep(1)

        logging.info("Accelerate Car")
        car.changeSpeed(speed, 1000)
        
        track_ids = []
        current_piece = 33

        while(True):
            logger_temp = logger
            r_piece = logger_temp.piece
            r_location = logger_temp.location
            r_clockwise = logger_temp.clockwise

            if r_piece != current_piece:
                if r_piece != 0 and (r_piece != 34 and len(track_ids) > 0):
                    track_ids.append(r_piece)
                current_piece = r_piece
            else:
                if r_piece == current_piece:
                    if (r_location < last_location and r_clockwise == False) or (r_location > last_location and r_clockwise == True):
                        logging.info("Double Trackpiece: {0}; Loc: {1}; last_loc: {2}, clockwise: {3}".format(r_piece, r_location, last_location, r_clockwise))
                        track_ids.append(r_piece)
                        current_piece = r_piece
            if r_piece == 34 and len(track_ids) > 1:
                logging.info("Scanning Track finished")
                break
            last_location = r_location

        
        logging.info("Stopping Car")
        car.changeSpeed(0, 1000)

        logging.info("Stopping Thread for Logging")
        log.join()

        

        has_33 = False
        has_34 = False

        for id in track_ids:
            if id == 33:
                has_33 = True
            if id == 34:
                has_34 = True

        if has_33 == False:
            track_ids.reverse()
            track_ids.append(33)
            track_ids.reverse()
        
        if has_34 == False:
            track_ids.append(34)


        track = Track(track_ids)
        
        result = ""
        str_track = ""

        if track_ids == expected_track:
            result = "PASS"
            
        else:
            result = "FAIL"            
            for x in track_ids:
                str_track = str_track + str(x) + ", "
            
        
        logging.info("Test {0}: {1}".format(i, result))
        test_log = test_log + "Result: " + result + "\n"

        if result == "FAIL":
            test_log = test_log + "Track: " + str_track + "\n\n"
        
    print(test_log)
    

