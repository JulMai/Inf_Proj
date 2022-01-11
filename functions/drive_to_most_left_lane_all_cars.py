import time
import os
from threading import Thread

from Vehicle.vehicle import Vehicle
from Track.trackPieceFactory import get_TrackPiece

class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    left_lane = False

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        global track

        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        t_piece = get_TrackPiece(piece)

        if not t_piece is None:
            lanes = t_piece.coordinates

            #print("piece: {0}, clockwise: {1}, location: {2}".format(piece, clockwise, location))

            if not(clockwise == True and (location in lanes[len(lanes)-1])) and not(clockwise == False and (location in lanes[0])):
                self.car.changeLaneLeft(speed, 1000)
            else:
                self.left_lane = True

def drive_to_most_left_lane_all_cars(cars, speed=300):
    car_loggers = {}
    for car in cars:
        car_logger = Car_Logger(kwargs={'car': car})
        car_loggers[car.addr] = car_logger
        car_logger.start()
        car.changeSpeed(speed, 1000)
        time.sleep(0.2)

    while not all(car_logger.left_lane == True for car_logger in car_loggers.values()):
        pass

    for car in cars:
        car.changeSpeed(0, 1000)
        car_loggers[car.addr].join()
