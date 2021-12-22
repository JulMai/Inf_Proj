from threading import Thread

class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False

    def run(self):
        self.car = self._kwargs['car']
        self.car.setLocationChangeCallback(self.locationChangeCallback)
    
    def locationChangeCallback(self, addr, location, piece, speed, clockwise):

        self.car.location = location
        self.car.piece = piece
        self.car.speed = speed
        self.car.clockwise = clockwise