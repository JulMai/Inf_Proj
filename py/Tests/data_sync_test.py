from overdrive import Overdrive
from test_Car_Logger import Car_Logger





if __name__ == "__main__":
    car = Overdrive("D9:A6:FA:EB:FC:01")
    if car._connected: print("Car1 connected")
    car_l = Car_Logger(car)
    car.changeSpeed(200, 1000)
