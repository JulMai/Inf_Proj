from vehicle import Vehicle
from Car_Logger.Car_Logger_Scan import scan_track

# class for simulation logic and communication between gui and vehicles
class Coordinator:

    def __init__(self):
        # the original vehicle list that contains all real vehicles
        self.vehicleList = []
        self.trackId = -1
        self.trackList = {}
        self.currentMode = None
        self.trafficLightMode = None
        self.intersectionMode = None
    
    # This method creates a vehicle with a specific mac address and adds it in the list of all vehicles
    def createVehicle(self, macAddress):
        self.vehicleList.append(Vehicle(macAddress))

    # This method starts the simulation and lets the vehicles drive with the current mode
    def startSimulation(self):
        
        return

    # This method stops the simulation and disconnects the vehicles from the server
    def stopSimulation(self):
        for v in self.vehicleList:
            v.disconnect()
        return

    # This method sets the simulation mode that the vehicles must follow
    def setMode(self, mode):
        self.currentMode = mode
        return
        
    # This method sets the speed of the chosen vehicle
    def setVehicleSpeed(self, speed, vehicleMacAddress):
        for v in self.vehicleList:
            if v.addr == vehicleMacAddress:
                v.desired_speed = speed
                break

    # This method sets the distance between the chosen vehicle and the vehicle in front of it
    def setVehicleDistance(self, distance, vehicleMacAddress):
        for v in self.vehicleList:
            if v.addr == vehicleMacAddress:
                v.distance = distance
                break

    # This method monitors the vehicles in terms of speed, distance, position, etc. and controls them
    def simulationLogic(self):
        return

    def start_ScanTrack(self):
        vehicle = self.vehicleList[0]
        return scan_track(vehicle)

        