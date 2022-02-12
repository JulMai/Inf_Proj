# Class for receiving Live-Car-Updates, Scanning the Track and writing the TrackPieces to a dictionary

from threading import Thread
import logging
import time

from functions.drive_to_most_left_lane import drive_to_most_left_lane
from functions.drive_to_start import drive_to_start

class Car_Logger_Scan(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    
    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
        self.track_ids = []
    
    # gets called everytime there is an update sent by the car
    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        #logging.info("Piece: {0}, Location: {1},Clockwise: {2}".format(piece, location ,clockwise))

        self.track_ids.append((piece, location, clockwise))

        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise   

# takes care of starting the Thread for Scanning
def setup_and_start_Car_Logger(car):
    c_l = Car_Logger_Scan(kwargs={'car': car})
    c_l.start()
    logging.info("Started Car_Logger_Scan-Thread for Car: {0}".format(car.addr))
    return c_l

# stops the Scanning-Thread
def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))
    del car_Logger
    
# Converts a list of TrackPiece-Numbers to a Dictionary
# Key: IIPPLL (I: Index, P: Position/TrackPiece, L: Location inside TrackPiece)
# Value: None, Space for Car-Obj or MAC-Address
def track_to_dict(track):
    track_dict = {}
    prev_piece = 0
    prev_loc = 0
    i = 0
    for l in track:
        str = f"{i:02d}{l[0]:02d}{l[1]:02d}"
        track_dict[str] = None
        prev_piece = l[0]
        prev_loc = l[1]
        i += 1
    return track_dict

# Function to scan the TrackPieces into a list
def scan_track(car, speed=400):
    # position Car properly to start scan (most left lane and piece 33/34)
    drive_to_most_left_lane(car)
    drive_to_start(car)

    car_logger = setup_and_start_Car_Logger(car)
    
    # Accelerate the car
    car.changeSpeed(speed, 1000)
    
    # keep driving until the car is back at the start/finish
    while (car_logger.piece != 34):
        pass
    
    # stop the car
    car.changeSpeed(0, 1000)
    time.sleep(1)
    track = car_logger.track_ids
    
    # if the TrackPieces 33 or 34 have not been scanned correctly, they get corrected here
    has_33 = False
    has_34_0 = False
    has_34_1 = False

    for loc in track:
        if loc[0] == 33:
            has_33 = True
        if loc[0] == 34:
            if loc[1] == 0:
                has_34_0 = True
            if loc[1] == 1:
                has_34_1 = True
            
    if not has_33:
        track = track.reverse()
        track.append((33, 0, False))
        track = track.reverse()
    
    if not(has_34_0 and has_34_1):
        if not has_34_0 and has_34_1:
            last = track.pop()
            track.append((34, 0, False))
            track.append(last)
        elif not has_34_0 and not has_34_1:
            track.append((34, 0, False))
            track.append((34, 1, False))

    track = track_to_dict(track)
    time.sleep(1)
    stop_and_cleanup_Car_Logger(car_logger)



    return track
