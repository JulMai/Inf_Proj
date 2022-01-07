import logging
import math
from threading import Thread

#from Car_Logger import Car_Logger
from intersection_handler import PriorityQueue


class Car_Logger_distance(Thread):

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
        self.track_c = self._kwargs['track']
        self.cars = self._kwargs['cars']
        self.lock = self._kwargs['lock']
        self.queue = self._kwargs['queue']

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        car_pos = self.add_car_to_track_c(
            self.track_c, piece, location, self.car.addr)
        #logging.info("Car {0}: Pos: {1}".format(self.car.addr, car_pos))

        abstand_r, car_ahead_speed = self.calc_distance_to_next_car(
            self.car, car_pos)

        new_speed_int, dist_to_intersection = self.handle_intersection(self.track_c, self.car, car_pos)
        new_speed_car = self.calc_new_speed(self.car, abstand_r, speed, car_ahead_speed)
        #if abstand_r > dist_to_intersection:

        if new_speed_int == None or new_speed_car == None:
            if new_speed_int == None:
                new_speed = new_speed_car
            elif new_speed_car == None:
                new_speed = new_speed_car
            else:
                new_speed = None
        else:
            new_speed = min(new_speed_int, new_speed_car)

        #if not new_speed:
            #new_speed = self.calc_new_speed(self.car, abstand_r, speed, car_ahead_speed)

        if new_speed:
            self.car.changeSpeed(new_speed, 1000)
            logging.info("Car {0}: Change Speed to {1}".format(addr, new_speed))

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
                    #logging.info(str(track_c))
                else:
                    new_pos = ""

        #logging.info("Lock released")
        if new_pos != "":
            return new_pos
        else:
            return old_pos

    def compare_pos_loc_with_str(self, piece, location, pos_str):
        return int(pos_str[2:4]) == piece and int(pos_str[4:6]) == location

    def calc_distance_to_next_car(self, car, car_pos):
        abstand_r = 100
        car_ahead_speed = 0
        i = self.get_pos_index_in_track_c(car_pos)

        car_spots = list(self.track_c.values())
        for j in range(i + 1, min(len(self.track_c), i + car.abstand + 1)):
            if car_spots[j] != None and car_spots[j] != car.addr:
                car_ahead_speed = self.cars[car_spots[j]].speed
                abstand_r = j - i
                break

        if abstand_r == 0 and car.abstand > (len(car_spots) - i):
            k = (len(car_spots) - i)
            for j in range(0, car.abstand + 1 - k):
                if car_spots[j] != None and car_spots[j] != car.addr:
                    car_ahead_speed = self.cars[car_spots[j]].speed
                    abstand_r = j + k
                    break
        if abstand_r != 100:
            pass
            #logging.info("Car {0}: Distance {1} to {2}".format(car.addr, abstand_r, car_spots[j]))
        return abstand_r, car_ahead_speed
    
    def get_next_pos(self, track_c, car_pos):
        pass

# +++ INTERSECTION +++

    def handle_intersection(self, track_c, car, car_pos):
        dist = self.calc_distance_to_intersection(track_c, car, car_pos)
        prio = self.queue.add(self.car, dist)

        if prio > 0:
            if dist == 0 or dist == 1:
                logging.info("Car {0}: wait on intersection".format(self.car.addr))
                return 0, dist
            else:
                if dist < 5:
                    return self.calc_new_speed_intersection_ahead(dist, car.speed), dist
                else:
                    return car.speed, dist
        else:
            return None, dist


    def calc_distance_to_intersection(self, track_c, car, car_pos):
        car_pos_i = self.get_pos_index_in_track_c(car_pos)
        next_intersection_i = self.get_pos_index_next_intersection(track_c, car_pos_i)

        if next_intersection_i is None:
            return 100

        if next_intersection_i < car_pos_i:
            return len(track_c) - car_pos_i + next_intersection_i
        else:
            return next_intersection_i - car_pos_i

    def get_pos_index_next_intersection(self, track_c, car_pos_index):
        list_tck = list(track_c.keys())

        for i in range(car_pos_index, len(list_tck)):
            if int(list_tck[i][2:4]) == 10:
                return i

        for i in range(car_pos_index - 1):
            if int(list_tck[i][2:4]) == 10:
                return i

        return None

    def calc_new_speed_intersection_ahead(self, dist_to_intersection, speed):    
        max_speed = speed
        min_speed = 200
        max_dist = 5
        min_dist = 2
        exp = 3

        if dist_to_intersection == max_dist:
            return speed
        
        a = (max_speed - min_speed) / pow(max_dist - 0.5 - min_dist, exp)
        return int(a * pow(dist_to_intersection - min_dist, exp) + min_speed)
        

# +++ INTERSECTION +++


    def calc_new_speed(self, car, abstand_r, speed_before, car_ahead_speed):
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
            new_speed = int(max(faktor * speed_before, 200))
            logging.info("Car {0}: (too close) Change Speed to {1}; Abstand_Ist: {2}; Faktor: {3}".format(
                car.addr, new_speed, abstand_r, faktor))
            return new_speed

    def remove_car_from_track_c(self, car):
        for x in self.track_c:
            if self.track_c[x] == car:
                self.track_c[x] = None

    def get_car_pos_in_track_c(self, car_addr):
        for pos in list(self.track_c.keys()):
            if self.track_c[pos] == car_addr:
                return pos
        return -1

    def get_pos_index_in_track_c(self, pos):
        i = 0
        for p in list(self.track_c.keys()):
            if p == pos:
                return i
            i += 1
        return -1


def setup_and_start_Car_Logger(car, cars, track, lock, queue):
    c_l = Car_Logger_distance(
        kwargs={'car': car, 'cars': cars, 'track': track, 'lock': lock, 'queue': queue})
    c_l.start()
    logging.info(
        "Started Car_Logger_distanc-Thread for Car: {0}".format(car.addr))
    return c_l


def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    del car_Logger
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="./logs/abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
