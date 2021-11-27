from vehicle import Vehicle
from test_Car_Logger import Car_Logger
from threading import Thread
import time

def log_v(v):
    logger = Car_Logger(v)

def add_car(address):
    cars.append(Vehicle(address))
    logs.append(Thread(target=log_v, args=(cars[-1],)))

def start_car(car_id, speed):
    logs[car_id].start()
    cars[car_id].changeSpeed(speed, 1000)
    

cars = []
logs = []

add_car("EC:33:B4:DB:9E:C8")
start_car(0, 400)

time.sleep(5)

for i in range(len(cars)):
    cars[i].changeSpeed(0, 1000)
    logs[i].join()

print("All Threads joined")