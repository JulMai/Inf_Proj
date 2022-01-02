import logging
import math
from threading import Thread

from Car_Logger import Car_Logger


class Car_Logger_distance(Thread):

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
        self.track_c = self._kwargs['track']
        self.cars = self._kwargs['cars']

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        i = 0
        j = 0
        a = 0

        car_pos = self.add_car_to_track_c(
            self.track_c, piece, location, self.car.addr)
        #logging.info("Car {0}: Pos: {1}".format(self.car.addr, car_pos))

        abstand_r, car_ahead_speed = self.calc_distance_to_next_car(
            self.car, car_pos)
        
        self.handle_intersection(self.car, car_pos)

        new_speed = self.calc_new_speed(
            self.car, abstand_r, speed, car_ahead_speed)
        if new_speed:
            self.car.changeSpeed(new_speed, 1000)

    def add_car_to_track_c(self, track_c, piece, location, car_addr):
        i = 0

        old_pos = self.get_car_pos_in_track_c(car_addr)
        i_old_pos = self.get_pos_index_in_track_c(old_pos)
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

        if self.compare_pos_loc_with_str(piece, location, new_pos_prediction):
            new_pos = new_pos_prediction
        else:
            new_pos = ""
            for i in range(i_old_pos + 1, len(list_tck)):
                pos = list_tck[i]
                if self.compare_pos_loc_with_str(piece, location, pos):
                    new_pos = pos
            if new_pos == "":
                for i in range(i_old_pos - 1):
                    pos = list_tck[i]
                    if self.compare_pos_loc_with_str(piece, location, pos):
                        new_pos = pos

        if new_pos != "":
            self.remove_car_from_track_c(car_addr)
            track_c[new_pos] = car_addr
            logging.info(str(track_c))
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


    def handle_intersection(self, car, car_pos):
        i = self.get_pos_index_in_track_c(car_pos)
        track = list(self.track_c.keys())
        for j in range(i + 1, i + 4):
            if int(track[j][2:4]) == 10:
                distance_intersection = j - i
                




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
            new_speed = int(faktor * speed_before)
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


def setup_and_start_Car_Logger(car, cars, track):
    c_l = Car_Logger_distance(kwargs={'car': car, 'cars': cars, 'track': track})
    c_l.start()
    logging.info("Started Car_Logger_distanc-Thread for Car: {0}".format(car.addr))
    return c_l

def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    del car_Logger
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="./logs/abstand_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    

