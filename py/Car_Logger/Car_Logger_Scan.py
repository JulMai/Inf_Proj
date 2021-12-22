from threading import Thread
import logging

class Car_Logger_Scan(Thread):
    location = 0
    piece = 0
    speed = 0
    clockwise = False
    
    def run(self):
        super().run(self)
        self.track_ids = []

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        logging.info("Piece: {0}, Location: {1},Clockwise: {2}".format(piece, location ,clockwise))

        self.track_ids.append((piece, location, clockwise))

        self.piece = piece
        self.location = location
        self.speed = speed
        self.clockwise = clockwise   

def setup_and_start_Car_Logger(car):
    c_l = Car_Logger_Scan(kwargs={'car': car})
    c_l.start()
    logging.info("Started Car_Logger_distanc-Thread for Car: {0}".format(car.addr))
    return c_l

def stop_and_cleanup_Car_Logger(car_Logger):
    car_Logger.join()
    del car_Logger
    logging.info("Stopped Car_Logger for Car: {0}".format(car_Logger.car.addr))