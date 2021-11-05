from overdrive import Overdrive

class Car_Logger:
    location = 0
    piece = 0
    speed = 0
    clockwise = ""

    def __init__(self, car):
        car.setLocationChangeCallback(self.locationChangeCallback)
    

    def locationChangeCallback(self, addr, location, piece, speed, clockwise):
        # Print out addr, piece ID, location ID of the vehicle, this print everytime when location changed
        self.location = location
        self.piece = piece
        self.speed = speed
        self.clockwise = clockwise
        print("Location from " + addr + " : " + "Speed=" +str(speed)+ " Piece=" + str(piece) + " Location=" + str(location) + " Clockwise=" + str(clockwise))
    
    def get_data(self):
        return {"speed": self.speed, "piece": self.piece, "location": self.location, "clockwise": self.clockwise}

