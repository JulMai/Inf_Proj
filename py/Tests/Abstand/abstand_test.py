from threading import Thread
from vehicle.vehicle import Vehicle
import time
import logging
from track.track import Track
from track.trackPieceFactory import get_TrackPiece
from read_lap_test_callback import scan_track_with_lanes
import os
import math


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
        
        #for x in track:
        #    if piece == x[0]:
        #        for l in range(len(x[1])):
        #            if x[1][l][0] == location:
        #               x[1][l][1] = self.car
        #                #print("Car1 assigned to Piece {0}, Location: {1}".format(piece, location))
        
        i = 0
        j = 0
        a = 0
        #logging.info("Car {0}: Piece: {1} Location: {2}".format(self.car.addr, piece, location))
        i = add_car_to_track_c((piece, location), self.car.addr)
        #logging.info(str(track_c))    

        abstand_r = 10
        car_ahead_speed = 0

        for j in range(i + 1, min(len(track_c), i + self.car.abstand + 1)):
            car_spots = list(track_c.values())

            if car_spots[j] != None and car_spots[j] != self.car.addr:
                abstand_r = j - i
                car_ahead_speed = cars[car_spots[j]].speed
                logging.info("Car: {0} Abstand_Ist: {1}".format(self.car.addr, abstand_r))

        if abstand_r == self.car.abstand:
            self.car.changeSpeed(car_ahead_speed, 1000)
        else:
            #if abstand_r <= 1:
            #    self.car.changeSpeed(150, 1000)
            #    time.sleep(0.5)
            #    self.car.changeSpeed(self.car.desired_speed, 1000)                
            #el
            if abstand_r < self.car.abstand:
                    # Abstand zu gering => langsamer werden

                    #abstand_quo = (abstand_r / self.car.abstand)
                    #new_speed = min(max(int(speed * abstand_quo), 0), 700)
                    # (1 - min.Anpassung)*log(Abstand_Ist;Abstand_Soll)+min.Anpassung                        
                    c = 0.6
                    faktor = (1 - c) * math.log(abstand_r, self.car.abstand) +c
                    new_speed = int(faktor * speed)
                    self.car.changeSpeed(new_speed, 1000)
                    logging.info("Car {0}: (too close) Change Speed to {1}; Abstand_Ist: {2}; Faktor: {3}".format(self.car.addr, new_speed, abstand_r, faktor))
            else:
                # Abstand in Ordnung => gewünschte Geschwindigkeit
                if abs(1 - (speed/self.car.desired_speed)) > 0.3:
                    self.car.changeSpeed(self.car.desired_speed, 1000)
                    logging.info("Car {0}: Abstand: i.O.; Change speed to {1}".format(self.car.addr, self.car.desired_speed))
                    

        self.car.piece = piece
        self.car.location = location
        self.car.speed = speed
        self.car.clockwise = clockwise



track = []
track_c = {}
cars = {}

def remove_car_from_track(car):
    global track
    
    
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
    global track_c
    i = 0
    piece = pos[0]
    location = pos[1]
    car_before = None
    new_pos = ""

    for x in list(track_c.keys()):
        if track_c[x] == car:
            car_before = x
        if car_before != None:
            if (int(x[2:4]) == piece and int(x[4:6]) == location):
                remove_car_from_track_c(car)            
                new_pos = x
                i += 1 
                break
        i += 1
    
    if new_pos == "":
        i = 0
        for x in list(track_c.keys()):
            if int(x[2:4]) == piece and int(x[4:6]) == location:
                remove_car_from_track_c(car)            
                new_pos = x
                i += 1 
                break
            i += 1


    if car_before == None:
        for x in list(track_c.keys()):
            if int(x[2:4]) == piece and int(x[4:6]) == location:
                new_pos = x
                i += 1
                break
            i += 1

    if new_pos != '' and new_pos != car_before:        
        track_c[new_pos] = car
        logging.info("Car: {0}: Position: {1}".format(car, new_pos))
    return i

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
    logging.basicConfig(filename="abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    
    
    #car1 = Vehicle("D9:A6:FA:EB:FC:01")
    car1 = Vehicle("C8:1C:54:E9:9B:2C")
    logging.info("Connected to Vehicle: \"{0}\"".format(car1.addr))
    car1.abstand = 1
    car1.desired_speed = 500

    car2 = Vehicle("EC:33:B4:DB:9E:C8")
    logging.info("Connected to Vehicle: \"{0}\"".format(car2.addr))
    car2.abstand = 3
    car2.desired_speed = 400

    cars = {car1.addr: car1, car2.addr: car2}

    logging.info("Scanning track")
    track_t = scan_track_with_lanes(car1)
        
    track = get_track_with_lanes(track_t)

    track_c = get_track_dict(track_t)

    

    time.sleep(1)

    
    car2_logger = Car_Logger(kwargs={'car': car2})
    car1_logger = Car_Logger(kwargs={'car': car1})    
    car1_logger.start()
    car2_logger.start()
    logging.info("Started Threads for Car_Loggers")

    logging.info("Accel Cars")
    car1.changeSpeed(500, 1000)
    car2.changeSpeed(400, 1000)

    time.sleep(30)

    logging.info("Stop Cars And wait")
    car1.changeSpeed(0, 1000)
    car2.changeSpeed(0, 1000)
    time.sleep(5)

    logging.info("Close Threads for Car_Loggers")
    car1_logger.join()
    car2_logger.join()
    logging.info("finished")
    os._exit(0)