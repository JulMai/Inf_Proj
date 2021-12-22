import logging
import threading
import time
from overdrive import Overdrive



def thread_function(name, mac):
    logging.info("Thread %s: starting", name)
    car = Overdrive(mac)
    if car._connected:
        logging.info("Car: %s is connected", mac)
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

    cars = {0: "D9:A6:FA:EB:FC:01", 1: "EC:33:B4:DB:9E:C8"}

    threads = list()
    for index in range(2):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index, cars[index]))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
