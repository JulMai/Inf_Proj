
from Car_Logger import Car_Logger

class Car_logger_distance(Car_Logger):

    def run(self):
        super()
        self.track_c = self._kwargs['track']

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        i = 0
        j = 0
        a = 0

        car_pos = self.add_car_to_track_c(self.track_c, piece, location, self.car.addr)
        #logging.info("Car {0}: Pos: {1}".format(self.car.addr, car_pos))

        abstand_r, car_ahead_speed = calc_distance_to_next_car(
            self.car, car_pos)

        new_speed = calc_new_speed(self.car, abstand_r, speed, car_ahead_speed)
        if new_speed:
            self.car.changeSpeed(new_speed, 1000)
        
    def add_car_to_track_c(track_c, piece, location, car_addr):
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
        pass
        #logging.info("Car {0}: Distance {1} to {2}".format(car.addr, abstand_r, car_spots[j]))
    return abstand_r, car_ahead_speed