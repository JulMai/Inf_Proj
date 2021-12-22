from threading import Thread
import time
import logging
import os
import math

from vehicle.vehicle import Vehicle
from track.track import Track
from track.trackPieceFactory import get_TrackPiece
from read_lap_test_callback import scan_track_with_lanes
from functions.drive_to_start import drive_to_start

cars = {}
track_c_direction = {}


class Car_Logger_Dist(Thread):
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

        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        #logging.info("Car {0}: Piece: {1} Location: {2}".format(addr, piece, location))

        # for x in track:
        #    if piece == x[0]:
        #        for l in range(len(x[1])):
        #            if x[1][l][0] == location:
        #               x[1][l][1] = self.car
        #                #print("Car1 assigned to Piece {0}, Location: {1}".format(piece, location))

        i = 0
        j = 0
        a = 0

        car_pos = add_car_to_track_c(piece, location, self.car.addr)
        #logging.info("Car {0}: Pos: {1}".format(self.car.addr, car_pos))

        abstand_r, car_ahead_speed = calc_distance_to_next_car(
            self.car, car_pos)

        new_speed = calc_new_speed(self.car, abstand_r, speed, car_ahead_speed)
        if new_speed:
            self.car.changeSpeed(new_speed, 1000)

        ## debug
        car_positions = []
        pi = 0
        for p in track_c.keys():
            if track_c[p] != None:
                car_positions.append((p, track_c[p]))
                pi += 1

        logging.info("Cars: {0}".format(car_positions))        

        if abstand_r != 100:
            logging.info("Car {0}: Abstand_Ist: {1}".format(
                self.car.addr, abstand_r))
        ## debug


track = []
track_c = {}
cars = {}


def calc_distance_to_next_car(car, car_pos):
    global track_c
    abstand_r = 100
    car_ahead_speed = 0
    i = get_pos_index_in_track_c(car_pos)

    car_spots = list(track_c.values())
    for j in range(i + 1, min(len(track_c), i + car.abstand + 1)):
        if car_spots[j] != None and car_spots[j] != car.addr:
            car_ahead_speed = cars[car_spots[j]].speed
            abstand_r = j - i            
            break

    if abstand_r == 0 and car.abstand > (len(car_spots) - i):
        k = (len(car_spots) - i)
        for j in range(0, car.abstand + 1 - k):
            if car_spots[j] != None and car_spots[j] != car.addr:
                car_ahead_speed = cars[car_spots[j]].speed
                abstand_r = j + k                
                break
    if abstand_r != 100:
        logging.info("Car {0}: Distance {1} to {2}".format(car.addr, abstand_r, car_spots[j]))
    return abstand_r, car_ahead_speed


def calc_new_speed(car, abstand_r, speed_before, car_ahead_speed):
    if abstand_r > car.abstand:
        # Abstand in Ordnung => gewünschte Geschwindigkeit
            if abs(1 - (speed_before/car.desired_speed)) > 0.1:
                logging.info("Car {0}: kein Auto voraus; Change speed to {1}".format(
                    car.addr, car.desired_speed))
                return car.desired_speed

    if abstand_r == car.abstand:
        logging.info("Car {0}: Abstand: wie gewünscht; Change speed to {1}".format(
            car.addr, car_ahead_speed))
        return car_ahead_speed

    if abstand_r < car.abstand:
        # Abstand zu gering => langsamer werden
        c = 0.6
        faktor = (1 - c) * math.log(abstand_r, car.abstand) + c
        new_speed = int(faktor * speed_before)
        logging.info("Car {0}: (too close) Change Speed to {1}; Abstand_Ist: {2}; Faktor: {3}".format(
            car.addr, new_speed, abstand_r, faktor))
        return new_speed
            


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


def add_car_to_track_c(piece, location, car_addr):
    global track_c
    i = 0

    old_pos = get_car_pos_in_track_c(car_addr)
    i_old_pos = get_pos_index_in_track_c(old_pos)
    #old_pos_clockwise = get_pos_clockwise(old_pos)
    # List of track_c Keys
    list_tck = list(track_c.keys())

    # if old_pos_clockwise:
    #    stp = -1
    # else:
    #    stp = 1
    if i_old_pos + 1 > len(list_tck) - 1:
        new_pos_prediction = list_tck[0]
    else:
        new_pos_prediction = list_tck[i_old_pos + 1]

    if compare_pos_loc_with_str(piece, location, new_pos_prediction):
        new_pos = new_pos_prediction
    else:
        new_pos = ""
        for i in range(i_old_pos + 1, len(list_tck)):
            pos = list_tck[i]
            if compare_pos_loc_with_str(piece, location, pos):
                new_pos = pos
        if new_pos == "":
            for i in range(i_old_pos - 1):
                pos = list_tck[i]
                if compare_pos_loc_with_str(piece, location, pos):
                    new_pos = pos

    if new_pos != "":
        remove_car_from_track_c(car_addr)
        track_c[new_pos] = car_addr
        return new_pos
    else:
        return old_pos

    # for i in range(i_old_pos + 1, len(list_tck)):
    #    if compare_pos_loc_with_str(piece, location, list_tck[i]):
    #        remove_car_from_track_c(car_addr)
    #        track_c[list_tck[i]] = car_addr
    #        logging.info("Car {0}: Position: {1}".format(car_addr, list_tck[i]))
    #        return list_tck[i]

    # for i in range(0, i_old_pos):
    #    if compare_pos_loc_with_str(piece, location, list_tck[i]):
    #        remove_car_from_track_c(car_addr)
    #        track_c[list_tck[i]] = car_addr
    #        logging.info("Car {0}: Position: {1}".format(car_addr, list_tck[i]))
    #        return list_tck[i]


def get_pos_clockwise(position):
    global track_c_direction
    return track_c_direction[position]


def compare_pos_loc_with_str(piece, location, pos_str):
    return int(pos_str[2:4]) == piece and int(pos_str[4:6]) == location


def get_car_pos_in_track_c(car_addr):
    global track_c

    for pos in list(track_c.keys()):
        if track_c[pos] == car_addr:
            return pos
    return -1


def get_pos_index_in_track_c(pos):
    global track_c
    i = 0

    for p in list(track_c.keys()):
        if p == pos:
            return i
        i += 1
    return -1


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
        track_c_direction[str] = l[2]
        prev_piece = l[0]
        prev_loc = l[1]
    return track_dict


def get_Lane(piece, location):
    norm_piece = get_TrackPiece(piece)

    for ls in norm_piece.coordinates:
        for l in ls:
            if l == location:
                return ls


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

    cars = {car1.addr: car1, car2.addr: car2}

    drive_to_start(car1)

    logging.info("Scanning track")
    track_t = scan_track_with_lanes(car1)

    #track = get_track_with_lanes(track_t)

    #track_c = get_track_dict(track_t)

    track_c = track_to_dict(track_t)

    logging.info(str(track_c))

    time.sleep(1)

    car1_logger = Car_Logger_Dist(kwargs={'car': car1})
    car2_logger = Car_Logger_Dist(kwargs={'car': car2})
    car1_logger.start()
    car2_logger.start()
    logging.info("Started Threads for Car_Loggers")

    logging.info("Accel Cars")
    car1.changeSpeed(car1.desired_speed, 1000)
    car2.changeSpeed(car2.desired_speed, 1000)

    time.sleep(600)

    logging.info("Stop Cars And wait")
    car1.changeSpeed(0, 1000)
    time.sleep(1)
    car2.changeSpeed(0, 1000)
    time.sleep(5)

    logging.info("Close Threads for Car_Loggers")
    car1_logger.join()
    car2_logger.join()
    logging.info("finished")
    os._exit(0)
