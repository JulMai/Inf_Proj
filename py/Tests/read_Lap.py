from overdrive import Overdrive
from test_Car_Logger import Car_Logger
import time
import logging

track_ids = []

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    car = Overdrive("D9:A6:FA:EB:FC:01")
    if car._connected: print("Car1 connected")
    car_l = Car_Logger(car)
    
    
    car.changeSpeed(200, 1000)

    #new_data = {"speed": 0, "piece": 0, "location": 0, "clockwise": ""}
    #old_data = {"speed": 0, "piece": 0, "location": 0, "clockwise": ""}

    current_id  = 33
    track_ids.append(current_id)
    
    i = 3000
    while (True):
        if car_l.piece == 34:
            track_ids.append(34)
            break
        else:
            piece = car_l.piece
            if current_id != piece:
                if piece != 0:
                    track_ids.append(piece)
                    current_id = piece



    
    car.changeSpeed(0, 1000)
    time.sleep(1)
    car.disconnect()
    del car

    print(track_ids)


