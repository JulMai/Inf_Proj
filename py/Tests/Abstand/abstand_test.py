from threading import Thread
from vehicle.vehicle import Vehicle
import time
import logging
from track.track import Track
from track.trackPieceFactory import get_TrackPiece
from read_lap_test_callback import scan_track_with_lanes
import os

car_on_track = False

class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
        
    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)  
          

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        global track
        global track_c
        global car_on_track
        
        if car_on_track == True:
            remove_car_from_track(self.car)
            remove_car_from_track_c(self.car.addr)         
        
        #for x in track:
        #    if piece == x[0]:
        #        for l in range(len(x[1])):
        #            if x[1][l][0] == location:
        #               x[1][l][1] = self.car
        #                car_on_track = True
        #                #print("Car1 assigned to Piece {0}, Location: {1}".format(piece, location))
        
        i = 0
        j = 0
        a = 0
        logging.info("Car {0}: Piece: {1} Location: {2}".format(self.car.addr, piece, location))



        for x in list(track_c.keys()):
            if int(x[2:4]) == piece and int(x[4:6]) == location and (not car_on_track or track_c[x] != self.car.addr):
                remove_car_from_track_c(self.car.addr)
                add_car_to_track_c(x, self.car.addr)
                #logging.info(str(track_c)) 
                break               
            i += 1
        for j in range(i + 1, min(len(track_c), i + self.car.abstand + 1)):
            car_spots = list(track_c.values())

            if car_spots[j] != None and car_spots[j] != self.car.addr:
                abstand_r = j - i
                logging.info("j-i: {0}".format(abstand_r))
                if abstand_r < self.car.abstand:
                    if abstand_r <= 0:
                        logging.info("Car {0}: too close => braking")                  
                        self.car.changeSpeed(0, 1000)
                        time.sleep(1)
                        logging.info("Car {0}: acc again")
                        self.car.changeSpeed(self.car.desired_speed, 1000)
                    else:
                        abstand_quo = 2 * (abstand_r / self.car.abstand)
                        new_speed = min(max(int(self.car.desired_speed * abstand_quo), 0), 700)
                        self.car.changeSpeed(new_speed, 1000)
                        logging.info("Car {0}: Change Speed to {1}; Abstand_r: {2}; Abstand_Quo: {3}".format(self.car.addr, new_speed, abstand_r, abstand_quo))                    
                else:
                    if abs(1 - (self.car.desired_speed / speed)) > 0.1:
                        self.car.changeSpeed(self.car.desired_speed, 1000)
                        logging.info("Car {0}: Abstand_r: {1}".format(self.car.addr, abstand_r))
            else:
                if abs(1 - (self.car.desired_speed / speed)) > 0.1:
                    self.car.changeSpeed(self.car.desired_speed, 1000)
                    logging.info("Car {0}: Abstand_r: {1}".format(self.car.addr, abstand_r))
                    

        self.car.piece = piece
        self.car.location = location
        self.car.speed = speed
        self.car.clockwise = clockwise



track = []
track_c = {}

def remove_car_from_track(car):
    global track
    global car_on_track
    
    
    for x in track:
        for y in x[1]:
            if y[1] == car:
                    y[1] = None

def remove_car_from_track_c(car):
    global track_c
    
    for x in track_c:
        if track_c[x] == car:
            track_c[x] = None

def add_car_to_track_c(pos, car):
    track_c[pos] = car

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

def get_track_dict(track_before):
    track_after = {}

    i = 0
    for t in track_before:
        id = t[0]
        location = t[1]
        piece = get_TrackPiece(id)
        for locations in piece.coordinates:
            for c in locations:
                if c == location:
                    for l in locations:
                        str = f"{i:02d}{id:02d}{l:02d}"
                        track_after[str] = None
        i+=1
    return track_after

   

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    car1 = Vehicle("D9:A6:FA:EB:FC:01")
    car1.abstand = 4
    car1.desired_speed = 500

    car2 = Vehicle("EC:33:B4:DB:9E:C8")
    car2.abstand = 3
    car2.desired_speed = 400

    track_t = scan_track_with_lanes(car1)
        
    track = get_track_with_lanes(track_t)

    track_c = get_track_dict(track_t)

    time.sleep(1)

    
    car2_logger = Car_Logger(kwargs={'car': car2})

    car1_logger = Car_Logger(kwargs={'car': car1})
    car1_logger.start()
    car2_logger.start()
    
    car1.changeSpeed(500, 1000)
    car2.changeSpeed(400, 1000)

    time.sleep(20)

    car1.changeSpeed(0, 1000)
    car2.changeSpeed(0, 1000)

    car1_logger.join()
    car2_logger.join()
    print("beendet")
    os._exit(0)