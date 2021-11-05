import logging
import threading
import time
from overdrive import Overdrive
from Car_Logger import Car_Logger

cars = {0: {"name": "D9:A6:FA:EB:FC:01", "speed": 0, "piece": 0, "location": 0}, 
        1: {"name": "EC:33:B4:DB:9E:C8", "speed": 0, "piece": 0, "location": 0}}



def thread_function(name, mac):
    logging.info("Thread %s: starting", name)
    car = Overdrive(mac)
    if car._connected:
        logging.info("Car: %s is connected", mac)
        car_l = Car_Logger(car)
        car.changeSpeed(400, 1000)
        time.sleep(5)
        car.changeSpeed(0, 1000)
        car.disconnect()
        del car
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(2):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index, cars[index]["name"]))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
