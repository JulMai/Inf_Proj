# Class for receiving Live-Car-Data

from threading import Thread
import logging

class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
    
    # gets called every time the car sents an update
    def locationChangeCallback(self, addr, location, piece, speed, clockwise):

        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise

        logging.info("Piece: {0}, Location: {1},Clockwise: {2}".format(piece, location ,clockwise))
