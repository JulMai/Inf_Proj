import logging
import threading, time
from test_Car_Logger import Car_Logger
from overdrive import Overdrive

class Logger(threading.Thread):
    def __init__(self, car, car_logger, *args, **kwargs):
        super(Logger,self).__init__(*args, **kwargs)
        self.shared = car

    def run(self):
        print(threading.current_thread(), 'start')
        car_l = Car_Logger(self.shared)
        time.sleep(10)
        print(threading.current_thread(), 'done')

class Reader(threading.Thread):
    def __init__(self, car, car_logger, *args, **kwargs):
        super(Reader,self).__init__(*args, **kwargs)
        self.shared = car

    def run(self):
        print(threading.current_thread(), 'start')
        
        
        print(threading.current_thread(), 'done')
    


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

car1 = Overdrive("D9:A6:FA:EB:FC:01")

if car1._connected: print("car connected")
threads = [ Logger(car=car1, name='a'), 
            Reader(car=car1, name='b')
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print('DONE')
