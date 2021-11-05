from overdrive import Overdrive
import time

def locationChangeCallback(addr, location, piece, speed, clockwise):
    # Print out addr, piece ID, location ID of the vehicle, this print everytime when location changed
    global loc
    loc = location
    
    global p
    p = piece

    #print("Location from " + addr + " : " + "Piece=" + str(piece) + " Location=" + str(location) + " Clockwise=" + str(clockwise))


car = Overdrive("EC:33:B4:DB:9E:C8")
if car._connected:
    print("connected")
#print(car.setLocationChangeCallback(locationChangeCallback)) # Set location change callback to function above
car.changeSpeed(500, 1000) # Set car speed with speed = 500, acceleration = 1000
loc = car.setLocationChangeCallback(locationChangeCallback)
i = 500
while (i > 0):
    loc = car.setLocationChangeCallback(locationChangeCallback)
    
    if loc != None:
        print(loc)
    time.sleep(0.01)
    i = i - 1



#car.changeLaneRight(1000, 1000) # Switch to next right lane with speed = 1000, acceleration = 1000
car.changeSpeed(0, 1000)
car.disconnect()
input() # Hold the program so it won't end abruptly
