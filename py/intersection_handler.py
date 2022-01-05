from threading import Lock
from Vehicle.vehicle import Vehicle

class PriorityQueue():
    
    def __init__(self, items):
        self.lock = Lock()
        self.queue = []
        self.items_to_queue(items)
        

    def add(self, item, priority):
        with self.lock:
            for i in range(len(self.queue)):
                if self.queue[i][0] == item:
                    self.queue.remove(self.queue[i])
                    break                 
            self.queue.append((item, priority))
            if len(self.queue) > 1:
                self.sort()
    
    def sort(self):
        self.queue.sort(key=lambda x: x[1])

    def items_to_queue(self, items):
        return {
            "Dictionary": self.dict_to_queue(items),
            #"List": self.list_to_queue(items),
        }.get(type(items))

    def dict_to_queue(self, items):
        q = []
        for i in items:
            self.add(i, items[i])

    #def list_to_queue(self, items):
    #    pass


if __name__ == "__main__":
    car1 = Vehicle("EC:33:B4:DB:9E:C8")
    car2 = Vehicle("D9:A6:FA:EB:FC:01")
    pq = PriorityQueue({car1: car1.dist_to_intersection, car2: car2.dist_to_intersection})
    pq.add(car1, 3)
    pq.add(car2, 2)
    pq.add(car1, 1)
    print("")