from threading import Thread
import logging

from functions.drive_to_most_left_lane import drive_to_most_left_lane
from functions.drive_to_start import drive_to_start

class Car_Logger_Scan(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    
    def run(self):
        super().run(self)
        self.track_ids = []

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        logging.info("Piece: {0}, Location: {1},Clockwise: {2}".format(piece, location ,clockwise))

        self.track_ids.append((piece, location, clockwise))

        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise   

def setup_and_start_Car_Logger(car):
    c_l = Car_Logger_Scan(kwargs={'car': car})
    c_l.start()
    logging.info("Started Car_Logger_distanc-Thread for Car: {0}".format(car.addr))
    return c_l

def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    del car_Logger
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))

def track_to_dict(track):
    global track_c_direction
    track_dict = {}
    prev_piece = 0
    prev_loc = 0
    i = 0
    for l in track:
        if prev_piece != 0:
            if l[0] == prev_piece:
                if abs(l[1] - prev_loc) != 1:
                    i += 1
            else:
                i += 1
        str = f"{i:02d}{l[0]:02d}{l[1]:02d}"
        track_dict[str] = None
        prev_piece = l[0]
        prev_loc = l[1]
    return track_dict

def scan_track(car):
    # Position Car properly to start scan
    drive_to_most_left_lane(car)
    drive_to_start(car)

    car_logger = setup_and_start_Car_Logger(kwargs={'car': car})

    while (car_logger.piece != 34 and len(car_logger.track_ids)<4):
        pass

    track = track_to_dict(car_logger.track_ids)
    stop_and_cleanup_Car_Logger(car_logger)

    return track
