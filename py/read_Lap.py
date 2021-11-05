from typing import Match
from overdrive import Overdrive
from Car_Logger import Car_Logger
import time

lap = {}

def get_piece_info(id):
    return {
        48: 'straight',
        17: 'turn',
        18: 'turn',
        34: 'start',
        20: 'turn'
    }.get(id, '')

       

if __name__ == "__main__":
    car = Overdrive("D9:A6:FA:EB:FC:01")
    if car._connected: print("Car1 connected")
    car_l = Car_Logger(car)
    
    run = True
    car.changeSpeed(300, 1000)

    new_data = {"speed": 0, "piece": 0, "location": 0, "clockwise": ""}
    old_data = {"speed": 0, "piece": 0, "location": 0, "clockwise": ""}

    start_piece = 0

    i = 3000
    while (run):
        old_data = new_data
        new_data = car_l.get_data()

        if start_piece == 0:
            start_piece = new_data["piece"]
            old_data = new_data
        
        
        if new_data["piece"] != old_data["piece"]:
            piece = new_data["piece"]
            
            if piece == start_piece:
                run = False
            else:
                lap[piece] = get_piece_info(piece)


    
    car.changeSpeed(0, 1000)
    time.sleep(1)
    car.disconnect()
    del car

    print(lap)


