from threading import Lock
import time
import logging
import os
import sys
import concurrent.futures

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)

from functions.drive_to_start import drive_to_start
from functions.drive_to_most_left_lane import drive_to_most_left_lane
from functions.drive_to_most_left_lane_all_cars import drive_to_most_left_lane_all_cars
from Car_Logger.Car_Logger_Scan import scan_track
from Car_Logger.Car_Logger_distance import Car_Logger_distance
from Car_Logger.Car_Logger_distance import setup_and_start_Car_Logger as setup_and_start_Car_Logger_Dist
from Vehicle.vehicle import Vehicle

class PriorityQueue():    
    def __init__(self, items):
        self.lock = Lock()
        self.queue = []
        self.items_to_queue(items)
        #self.thread = Thread(target=self.remove_lowest_prio_periodically, args=(self.lock, self.queue))
        #self.thread.start()

    #def __del__(self):
        #self.thread.join()
        
    
    def remove_lowest_prio_periodically(self, lock, queue):
        last_highest_prio = queue[0]
        while True:
            time.sleep(1.5)
            with lock:
                if len(queue) > 0 and last_highest_prio == queue[0]:
                    logging.info("Removing {0} from PriorityQueue".format(queue[0][0].addr))
                    queue.pop(0)
                    if len(queue) > 0:
                        last_highest_prio = queue[0]
                    

    def add(self, item, priority):
        with self.lock:
            for i in range(len(self.queue)):
                if self.queue[i][0] == item:
                    self.queue.pop(i)
                    break                 
            self.queue.append((item, priority, time.time()))
            if len(self.queue) > 1:
                self.sort()
            return self.get_index_of_item(item)
    
    def remove(self, item):
        with self.lock:
            self.queue.pop(self.get_index_of_item(item))
    

    def get_index_of_item(self, item):
        for i in range(len(self.queue)):
            if self.queue[i][0] == item:
                return i
        return -1

    def get_prio_of_item(self, item):
        return self.get_index_of_item(item)
    
    def sort(self):
        #with self.lock:
        #last_highest_prio = self.queue[0]

        self.queue.sort(key=lambda x: (x[1], x[2]))
        logging.info(self.queue_to_string())

    def items_to_queue(self, items):
        return {
            "Dictionary": self.dict_to_queue(items),
            #"List": self.list_to_queue(items),
        }.get(type(items))

    def dict_to_queue(self, items):
        for i in items:
            self.add(i, 0)

    def queue_to_string(self):
        to_string = ""
        for i in self.queue:
            to_string += "('{0}': {1}, {2}), ".format(i[0].addr, i[1], i[2])
        #to_string += " " + str(len(self.queue))
        return to_string

car_loggers = []
executor = None

def helper(args):
    setup_and_start_Car_Logger_Dist(args[0], args[1], args[2], args[3], args[4])

def startSim(cars, track_c):   

    lock = Lock()
    queue = PriorityQueue(cars)

    drive_to_most_left_lane_all_cars(cars)

    cars_dict = {}
    for car in cars:
        cars_dict[car.addr] = car
    
    car1 = cars[0]
    car2 = cars[1]
    car3 = cars[2]

    car1_logger = setup_and_start_Car_Logger_Dist(car1, cars_dict, track_c, lock, queue)
    car2_logger = setup_and_start_Car_Logger_Dist(car2, cars_dict, track_c, lock, queue)
    car3_logger = setup_and_start_Car_Logger_Dist(car3, cars_dict, track_c, lock, queue)
    logging.info("Started Threads for Car_Loggers")

    logging.info("Accelerate Cars")
    for car in cars:
        car.changeSpeed(car.desired_speed, 1000)
        #print("Car {0}: Change Speed to {1}".format(car.addr, car.desired_speed))
        time.sleep(0.2)

def stopSim(cars):
    for car in cars:
        car.changeSpeed(0, 1000)
        time.sleep(1)
    for car_l in car_loggers:
        car_l.join()


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename="distance_testing.log", filemode="w", format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    car1 = Vehicle("D9:A6:FA:EB:FC:01")
    #car1 = Vehicle("C8:1C:54:E9:9B:2C")
    logging.info("Connected to Vehicle: \"{0}\"".format(car1.addr))
    car1.distance = 2
    car1.desired_speed = 500

    car2 = Vehicle("EC:33:B4:DB:9E:C8")
    logging.info("Connected to Vehicle: \"{0}\"".format(car2.addr))
    car2.distance = 2
    car2.desired_speed = 400

    car3 = Vehicle("C8:1C:54:E9:9B:2C")
    logging.info("Connected to Vehicle: \"{0}\"".format(car3.addr))
    car3.distance = 2
    car3.desired_speed = 350

    cars = [car1, car2, car3]

    drive_to_most_left_lane(car1)    
    #drive_to_start(car1)

    #logging.info("Scanning track")
    track_c = scan_track(car1)

    logging.info(str(track_c))

    time.sleep(1)    

    #drive_to_most_left_lane(car2)
    #drive_to_most_left_lane(car3)    

    startSim(cars, track_c)

    time.sleep(10)

    #stopSim(cars)

    #logging.info("Close Threads for Car_Loggers")
    #car1_logger.join()
    #car2_logger.join()
    #car3_logger.join()
    logging.info("finished")
    os._exit(0)
