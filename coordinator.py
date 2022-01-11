
from Vehicle.vehicle import Vehicle
from Car_Logger.Car_Logger_Scan import scan_track

from Simulations.first_come_first_serve import sim_mode0
from Car_Logger.Car_Logger_distance import setup_and_start_Car_Logger as setup_and_start_Car_Logger_Dist

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
    def startSimulation(self, mode=0):
        self.currentMode = {
            0: sim_mode0.startSim(self.vehicleList, self.trackList)
        }.get(mode)

    # This method stops the simulation and disconnects the vehicles from the server
    def stopSimulation(self):
        {
            0: sim_mode0.stopSim(self.vehicleList)
        }.get(self.currentMode)
        #for v in self.vehicleList:
        #    v.disconnect()
        

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

        