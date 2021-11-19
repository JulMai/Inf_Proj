from test_Car_Logger import Car_Logger
from overdrive import Overdrive
from threading import Thread
import logging

class car(Thread):
    def __init__(self, mac) -> None:
        self.car = Overdrive(mac)
        self.logger = Car_Logger(self.car)

    
        
