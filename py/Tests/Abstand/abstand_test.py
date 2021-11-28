from threading import Thread
from vehicle.vehicle import Vehicle
import time
import logging
from track.track import Track
from track.trackPieceFactory import get_TrackPiece
from read_lap_test_callback import scan_track_with_lanes

car_on_track = False

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
        global track
        global car_on_track
        
        if car_on_track == True:
            remove_car_from_track(car1)
        
        for x in track:
            if piece == x[0]:
                for l in range(len(x[1])):
                    if x[1][l][0] == location:
                        x[1][l][1] = car1
                        car_on_track = True
                        #print("Car1 assigned to Piece {0}, Location: {1}".format(piece, location))
                        print(str(track))
                      


        
        
        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise


track = []

def remove_car_from_track(car):
    global track
    global car_on_track
    
    
    for x in track:
        for y in x[1]:
            if y[1] == car:
                    y[1] = None
                    print("")


def get_track_with_lanes(track_before):
    track_after = []

    for t in track_before:
        id = t[0]
        location = t[1]
        piece = get_TrackPiece(id)
        lane = []
        for locations in piece.coordinates:
            for c in locations:
                if c == location:
                    for i in range(len(locations)):
                        locations[i] = [locations[i], None]
                    lane = locations
                    break
        track_after.append([id, lane])

    return track_after


if __name__ == "__main__":
    #car = Vehicle("D9:A6:FA:EB:FC:01")
    car1 = Vehicle("EC:33:B4:DB:9E:C8")

    track_t = scan_track_with_lanes(car1)

    
    track = get_track_with_lanes(track_t)

    time.sleep(1)

    car_logger = Car_Logger(kwargs={'car': car1})
    car_logger.start()

    car1.changeSpeed(400, 1000)

    time.sleep(10)

    car1.changeSpeed(0, 1000)

    car_logger.join()

    print("")