# Class for getting Car-Data-Updates and keeping distances to other cars and an intersection

import logging
import math
from threading import Thread
import time

#from Car_Logger import Car_Logger
from Simulations.first_come_first_serve.intersection_handler import PriorityQueue
from functions.drive_to_most_left_lane import drive_to_most_left_lane
from Track.trackPieceFactory import get_TrackPiece

class Car_Logger_distance(Thread):

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
        self.track_c = self._kwargs['track']
        self.cars = self._kwargs['cars']
        self.lock = self._kwargs['lock']
        self.queue = self._kwargs['queue']
        
        while True:
            time.sleep(0.2)

    # gets called everytime there is an update from the car
    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise
        
        # checking if the car is still in the left lane of the TrackPiece
        if not self.check_if_left_lane(piece, location, clockwise):
            self.car.changeLaneLeft(speed, 1000)
            return
        
        # Add the Cars Position to the value of Track-Dictionary to the new position key
        car_pos = self.add_car_to_track_c(
            self.track_c, piece, location, self.car.addr)
        #logging.info("Car {0}: Pos: {1}".format(self.car.addr, car_pos))
        
        # Calculate the distance to the next car and get the speed of that car
        dist_to_next_car, car_ahead_speed = self.calc_distance_to_next_car(
            self.car, car_pos)
        
        # Calculate the distance to the next intersection
        dist_to_intersection = self.calc_distance_to_intersection(
            self.track_c, self.car, car_pos)
        # add the car to the PriorityQueue and get back its priority
        prio = self.queue.add(self.car, dist_to_intersection)
        
        # Calculate the cars new speed based on its distance to the next car and the distance to the intersection
        new_speed = self.calc_new_speed(
            self.car, dist_to_next_car, speed, car_ahead_speed, dist_to_intersection, prio)
        
        # Send the new calculated speed to the car
        if not new_speed is None:
            if new_speed == 0:
                self.car.changeSpeed(int(new_speed), 1000)
                while(self.queue.get_prio_of_item(self.car) > 0):
                    time.sleep(0.1)
                new_speed = self.car.desired_speed
            self.car.changeSpeed(int(new_speed), 1000)            
            logging.info("Car {0}: Change Speed to {1}".format(addr, new_speed))

    # check if the position is on the most left lane of the TrackPiece
    def check_if_left_lane(self, piece, location, direction):
        t_piece = get_TrackPiece(piece)
        if not t_piece is None:
            lanes = t_piece.coordinates
        return not(not(direction == True and (location in lanes[len(lanes)-1])) and not(direction == False and (location in lanes[0])))
    
    # Add the car to the value of Track-Dictionary at the position (key)
    # starts search from the old position of the car
    def add_car_to_track_c(self, track_c, piece, location, car_addr):
        i = 0

        #logging.info("Lock aquired by {0}".format(self.car.addr))

        old_pos = self.get_car_pos_in_track_c(car_addr)
        i_old_pos = self.get_pos_index_in_track_c(old_pos)

        with self.lock:
            # List of track_c Keys
            list_tck = list(track_c.keys())
            new_pos = ""
            for i in range(i_old_pos + 1, len(list_tck)):
                pos = list_tck[i]
                if self.compare_pos_loc_with_str(piece, location, pos):
                    new_pos = pos
                    break
            if new_pos == "":
                for i in range(0, i_old_pos):
                    pos = list_tck[i]
                    if self.compare_pos_loc_with_str(piece, location, pos):
                        new_pos = pos
                        break

            if new_pos != "":
                if track_c[new_pos] == None:
                    self.remove_car_from_track_c(car_addr)
                    track_c[new_pos] = car_addr
                    # logging.info(str(track_c))
                else:
                    new_pos = ""

        #logging.info("Lock released")
        if new_pos != "":
            return new_pos
        else:
            return old_pos
    
    # check if the position (piece and location) is the same as in the position string
    def compare_pos_loc_with_str(self, piece, location, pos_str):
        return int(pos_str[2:4]) == piece and int(pos_str[4:6]) == location
    
    # Calculating the distance to the next car ahead and returning its speed
    # distance = amount of TrackPiece-Positions between the two cars in the Track-Dictionary
    def calc_distance_to_next_car(self, car, car_pos):
        dist_to_next_car = 100
        car_ahead_speed = 0
        i = self.get_pos_index_in_track_c(car_pos)

        car_spots = list(self.track_c.values())
        for j in range(i + 1, min(len(self.track_c), i + car.distance + 1)):
            if car_spots[j] != None and car_spots[j] != car.addr:
                car_ahead_speed = self.cars[car_spots[j]].speed
                dist_to_next_car = j - i
                break

        if dist_to_next_car == 0 and car.distance > (len(car_spots) - i):
            k = (len(car_spots) - i)
            for j in range(0, car.distance + 1 - k):
                if car_spots[j] != None and car_spots[j] != car.addr:
                    car_ahead_speed = self.cars[car_spots[j]].speed
                    dist_to_next_car = j + k
                    break
        if dist_to_next_car != 100:
            pass
            # logging.info("Car {0}: Distance {1} to {2}".format(car.addr, dist_to_next_car  car_spots[j]))
        return dist_to_next_car, car_ahead_speed

# +++ INTERSECTION +++
    
#    def handle_intersection(self, track_c, car, car_pos):
#        dist = self.calc_distance_to_intersection(track_c, car, car_pos)
#        prio = self.queue.add(self.car, dist)
#
#        if prio > 0:
#            if dist == 0 or dist == 1:
#                logging.info(
#                    "Car {0}: wait on intersection".format(self.car.addr))
#                return 0, dist
#            else:
#                if dist < 5:
#                    return self.calc_new_speed_intersection_ahead(dist, car.speed), dist
#                else:
#                    return car.speed, dist
#        else:
#            return None, dist
    
    # Calculating and Returning the distance of the car to the next intersection
    def calc_distance_to_intersection(self, track_c, car, car_pos):
        car_pos_i = self.get_pos_index_in_track_c(car_pos)
        next_intersection_i = self.get_pos_index_next_intersection(
            track_c, car_pos_i)

        if next_intersection_i is None:
            return 100

        if next_intersection_i < car_pos_i:
            return len(track_c) - car_pos_i + next_intersection_i
        else:
            return next_intersection_i - car_pos_i

    # get the PositionIndex of the next intersection in the Track-Dictionary
    def get_pos_index_next_intersection(self, track_c, car_pos_index):
        list_tck = list(track_c.keys())

        for i in range(car_pos_index, len(list_tck)):
            if int(list_tck[i][2:4]) == 10:
                return i

        for i in range(car_pos_index - 1):
            if int(list_tck[i][2:4]) == 10:
                return i

        return None

    # Calculating the cars new speed based on the distance to the intersection
    def calc_new_speed_intersection_ahead(self, dist_to_intersection, speed):
        max_speed = speed
        min_speed = 200
        max_dist = 5
        min_dist = 2
        exp = 3

        if dist_to_intersection >= max_dist:
            logging.info("Car {0}: keep speed".format(self.car.addr))
            return self.car.desired_speed
        elif dist_to_intersection < min_dist:
            logging.info(
                "Car {0}: Intersection close => stop".format(self.car.addr))
            return 0
        else:
            logging.info(
                "Car {0}: Intersection ahead => brake softly". format(self.car.addr))
            #a = (max_speed - min_speed) / pow(max_dist - 0.5 - min_dist, exp)
            #return int(a * pow(dist_to_intersection - min_dist, exp) + min_speed)
            return int(max_speed * math.log(dist_to_intersection, 10) + min_speed)

# --- INTERSECTION ---

    # Calculate the new speed of the cars based on 
    #  - the distance to the next car ahead
    #  - the speed the car had before
    #  - the distance to the intersection
    #  - the Priority in the PriorityQueue
    def calc_new_speed(self, car, dist_to_next_car, speed_before, car_ahead_speed, dist_to_intersection, prio):
        if dist_to_intersection > dist_to_next_car:
            return self.calc_speed_car_ahead(dist_to_next_car, car, speed_before, car_ahead_speed)
        else:
            if prio > 0:
                return self.calc_new_speed_intersection_ahead(dist_to_intersection, speed_before)
            else:
                return self.calc_speed_car_ahead(dist_to_next_car, car, speed_before, car_ahead_speed)

    # Calculating the speed if there is a car ahead ("Cruise Control")
    def calc_speed_car_ahead(self, dist_to_next_car, car, speed_before, car_ahead_speed):
        if dist_to_next_car > car.distance:
            # distance in Ordnung => gewünschte Geschwindigkeit
            if abs(1 - (speed_before/car.desired_speed)) > 0.1:
                logging.info("Car {0}: no car ahead".format(car.addr))
                return car.desired_speed
        elif dist_to_next_car == car.distance:
            logging.info("Car {0}: desired distance".format(car.addr))
            return car_ahead_speed
        elif dist_to_next_car < car.distance:
            # distance zu gering => langsamer werden
            c = 0.6
            faktor = (1 - c) * math.log(dist_to_next_car, car.distance) + c
            new_speed = int(max(faktor * speed_before, 200))
            logging.info("Car {0}: too close".format(
                car.addr, new_speed, dist_to_next_car, faktor))
            return new_speed
    
    # Remove the car from the Track-Dictionary
    def remove_car_from_track_c(self, car):
        for x in self.track_c:
            if self.track_c[x] == car:
                self.track_c[x] = None
    
    # Get the Position of a car in the Track-Dictionary
    def get_car_pos_in_track_c(self, car_addr):
        for pos in list(self.track_c.keys()):
            if self.track_c[pos] == car_addr:
                return pos
        return -1
    
    # Get the index of Position in the Track-Dicionary
    def get_pos_index_in_track_c(self, pos):
        i = 0
        for p in list(self.track_c.keys()):
            if p == pos:
                return i
            i += 1
        return -1

# Takes car of setting up and starting the Car-Logging-Thread
def setup_and_start_Car_Logger(car, cars, track, lock, queue):
    c_l = Car_Logger_distance(
        kwargs={'car': car, 'cars': cars, 'track': track, 'lock': lock, 'queue': queue})
    c_l.start()
    logging.info(
        "Started Car_Logger_distanc-Thread for Car: {0}".format(car.addr))
    return c_l

# Stops and deletes the Car-Logging-Thread
def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    del car_Logger
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))
