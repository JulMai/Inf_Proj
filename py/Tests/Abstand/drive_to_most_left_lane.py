import time
import os

from vehicle.vehicle import Vehicle
from track.trackPieceFactory import get_TrackPiece

if __name__ == '__main__':

    t = get_TrackPiece(18)

    car = Vehicle("EC:33:B4:DB:9E:C8")
    speed = 300


    os._exit(0)
    car.changeSpeed(speed, 1000)
    for i in range(0,15):
        car.changeLaneLeft(speed, 1000)
        time.sleep(1)

    car.changeSpeed(0, 1000)
    del car
    os._exit(0)
