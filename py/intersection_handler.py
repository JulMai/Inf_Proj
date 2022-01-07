import logging
from threading import Lock, Thread
import time

from Vehicle.vehicle import Vehicle

class PriorityQueue():    
    def __init__(self, items):
        self.lock = Lock()
        self.queue = []
        self.items_to_queue(items)
        self.thread = Thread(target=self.remove_lowest_prio_periodically, args=(self.lock, self.queue))
        self.thread.start()

    def __del__(self):
        self.thread.join()
        

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
            self.queue.append((item, priority))
            if len(self.queue) > 1:
                self.sort()
        return self.get_index_of_item(item)
    

    def get_index_of_item(self, item):
        with self.lock:
            for i in range(len(self.queue)):
                if self.queue[i][0] == item:
                    return i
            return -1            
    
    def sort(self):
        self.queue.sort(key=lambda x: x[1])
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
            to_string += "('{0}': {1}), ".format(i[0].addr, i[1])
        return to_string

if __name__ == "__main__":
    car1 = Vehicle("EC:33:B4:DB:9E:C8")
    car2 = Vehicle("D9:A6:FA:EB:FC:01")
    cars = {car1.addr: car1, car2.addr: car2}
    pq = PriorityQueue(list(cars.values()))
    pq.add(car1, 3)
    pq.add(car2, 2)
    pq.add(car1, 1)
    print(pq.queue_to_string())
    time.sleep(1.4)
    print(pq.queue_to_string())
    time.sleep(1.4)
    print(pq.queue_to_string())
    time.sleep(1.4)
    print(pq.queue_to_string())