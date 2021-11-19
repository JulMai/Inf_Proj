from overdrive import Overdrive
from datetime import datetime
import logging
from threading import Thread

class Car_Logger(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = ""
    last_refresh = datetime.now()
    refreshes = []

    def __init__(self, car):
        car.setLocationChangeCallback(self.locationChangeCallback)

    def run():
        pass
    

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        # Print out addr, piece ID, location ID of the vehicle, this print everytime when location changed
        self.location = location
        self.piece = piece
        self.speed = speed
        self.clockwise = clockwise
        refresh = datetime.now()
        diff = (refresh - self.last_refresh).microseconds / 1e+6
        self.refreshes.append(diff)
        self.last_refresh = refresh
        logging.info("{0}: Location from {1} : Speed={2} Piece={3} Location={4} Clockwise={5}".format(str(self.last_refresh), str(addr), str(speed), str(piece), str(location), str(clockwise)))
    
    def get_data(self):
        return {"speed": self.speed, "piece": self.piece, "location": self.location, "clockwise": self.clockwise}

    def get_refresh_rate(self):
        sum = 0.0
        for i in self.refreshes:
            sum = sum + i
        refresh_rate = sum / len(self.refreshes)
        return refresh_rate
        