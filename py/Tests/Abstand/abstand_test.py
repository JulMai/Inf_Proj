from threading import Thread
from vehicle.vehicle import Vehicle
import time
import logging
from track.track import Track
from track.trackPieceFactory import get_TrackPiece


class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    
    def run(self):
        self.track_ids = []
        car = self._kwargs['car']
        car.setLocationChangeCallback(self.locationChangeCallback)  
          

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        if self.check_id(piece) != '' and not (piece == 34 and len(self.track_ids)==0):
            if piece == self.piece:
                if (location > self.location and clockwise == True) or (location < self.location and clockwise == False):
                    self.track_ids.append((piece, location))               
            else:
                self.track_ids.append((piece, location))
        
        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise

    def check_id(self, id):
        return {        
            10: True,
            17: True,
            18: True,
            20: True,
            23: True,
            33: True,
            34: True,
            36: True,
            39: True,
            48: True
        }.get(id, '')     


def scan_track(car, speed=500):

    car_logger = Car_Logger(kwargs={'car': car})
    car_logger.start()

    car.changeSpeed(speed, 1000)

    time.sleep(1)

    car.changeSpeed(0, 1000)
    

    has_33 = False
    has_34 = False

    track_ids = car_logger.track_ids

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

    car_logger.join()
    del car_logger

    return track_ids

    

#car = Vehicle("D9:A6:FA:EB:FC:01")
car1 = Vehicle("EC:33:B4:DB:9E:C8")
car_logger = Car_Logger(kwargs={'car': car1})
car_logger.start()

car1.changeSpeed(400, 1000)

time.sleep(12)

car1.changeSpeed(0, 1000)

track_t = car_logger.track_ids

car_logger.join()

track_ids = []

track = []

for t in track_t:
    id = t[0]
    location = t[1]
    piece = get_TrackPiece(id)
    lane = []
    for l in piece.coordinates:
        for c in l:
            if c == location:
                lane = l
                break
    track.append([id, lane])
    print("")
    


print("")