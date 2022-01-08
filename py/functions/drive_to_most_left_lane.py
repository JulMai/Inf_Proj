import time
import os
from threading import Thread
import logging

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

        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        t_piece = get_TrackPiece(piece)

        if not t_piece is None:
            lanes = t_piece.coordinates

        print("piece: {0}, clockwise: {1}, location: {2}".format(piece, clockwise, location))

        if not(clockwise == True and (location in lanes[len(lanes)-1])) and not(clockwise == False and (location in lanes[0])):
            logging.info("Car {0}: Change Lane left".format(self.car.addr))
            self.car.changeLaneLeft(speed, 1000)
        else:
            self.left_lane = True


def drive_to_most_left_lane(car, speed=300):
    car_logger = Car_Logger(kwargs={'car': car})
    car_logger.start()
    car.changeSpeed(speed, 1000)

    while car_logger.left_lane == False:
        pass

    car.changeSpeed(0, 1000)
    car_logger.join()


if __name__ == '__main__':
    #car = Vehicle("EC:33:B4:DB:9E:C8")
    car = Vehicle("C8:1C:54:E9:9B:2C")
    drive_to_most_left_lane(car)
    time.sleep(1)
    del car

    os._exit(0)
