from tkinter import *
from tkinter.ttk import*
from coordinator import Coordinator
from tkinter.messagebox import askyesno
import Draw_Track.mapping as mapping
from threading import Thread
import time
import os

root = Tk()
root.title("Anki-Overdrive-Project")
# root.geometry("400x400")

update = True

class Gui:

    # Used to seperate the vehicles
    colors = ["red", "blue", "green", "purple", "yellow"]
    # radius for vehiclesCircles 
    radius = 10
    track_Coordinates = []
    # TODO
    vehicles = []
    str_status = ""
    list_canvas_checkpoints = []

    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.pack()

        #self.macAddressList = ["AB:CD:EF:GH", "12:34:56:78"]

        # create coordinator object to communicate with vehicles
        self.coordinator = Coordinator()

        # Track list
        self.trackList = []
        
        # Canvas for Track
        self.mapCanvas = Canvas(mainFrame)
        self.mapCanvas.grid(row=0, column=0)
        # Sidebar for Vehicledata and Settings Choices
        self.settingsFrame = Frame(mainFrame)
        self.settingsFrame.grid(row=0, column=1, sticky="n")

        # all Vehicle Frame
        self.vehicleDataFrame = Frame(self.settingsFrame)
        self.vehicleDataFrame.grid(row=0, column=0)

        # settings like mode, scantrack etc
        self.generalSettingsFrame = Frame(self.settingsFrame)
        self.generalSettingsFrame.grid(row=1, column=0)

        # Thread Version only works once
        #self.scanTrackButton = Button(self.generalSettingsFrame, text="Scan Track", command=threading.Thread(target=self.scanTrack).start)

        # noThread Version
        self.scanTrackButton = Button(
            self.generalSettingsFrame, text="Scan Track", command=self.scanTrack)
        self.scanTrackButton.grid(row=0, column=4)

        self.updateVehicleButton = Button(
            self.generalSettingsFrame, text="Update", command=self.sendValues)
        self.updateVehicleButton.grid(row=0, column=3)

        self.startButton = Button(self.generalSettingsFrame,text="Start",command=self.startSimulation)
        self.startButton.grid(row=0,column=0)
        
        self.stopButton = Button(self.generalSettingsFrame,text = "Stop", command=self.stopSimulation)
        self.stopButton.grid(row=0,column=2,padx=(0,20))

        for child in self.generalSettingsFrame.winfo_children():
            child.grid_configure(pady=5)

        # Testing
        
        self.createVehicle("D9:A6:FA:EB:FC:01")
        self.createVehicle("EC:33:B4:DB:9E:C8")
        self.createVehicle("C8:1C:54:E9:9B:2C")

        # TODO for macAddress in self.macAddressList:
        #    self.createVehicle(macAddress)

        # how to movecircle 2 forexample
        # TODO: create method where all available vehicles get updated
        # TODO self.updateVehicles()

        #thread_updateVehicle = Thread(target=self.updateVehicle, args=(self,))
        #thread_updateVehicle.start()
        

    def startSimulation(self):
        self.init_update()
        self.coordinator.startSimulation()
        

    def stopSimulation(self):
        global update
        update = False
        self.coordinator.stopSimulation()
    
    def init_update(self):
        thread = Thread(target=updateVehicles, args=(self,))
        thread.start()
        

    def scanTrack(self):
        # todo send msg to scan the track
        # get name of png

        # get scanned track list to create virtual map
        self.trackList_raw = self.coordinator.start_ScanTrack()
        self.coordinator.trackList = self.trackList_raw
        
        mapping.map_grid(self.trackList_raw)
        self.list_canvas_checkpoints = mapping.checkpoints()

        self.trackImage = PhotoImage(file=mapping._track)
        self.mapCanvas.config(width=self.trackImage.width(),
                              height=self.trackImage.height())
        self.mapCanvas.create_image(0, 0, image=self.trackImage, anchor="nw")
        
        self.fixCircles()

    def createVehicleFrame(self, mac):
        frame = self.vehicleDataFrame

        # init Variables for Display
        speed = StringVar()
        newSpeed = StringVar()
        distance = StringVar()
        macAdress = StringVar()
        macAdress.set(mac)

        i = len(self.vehicles)
        vehicleFrame = LabelFrame(frame, text=i)
        vehicleFrame.grid(row=i, column=0)

        labelColor = Label(vehicleFrame, text="Color")
        labelColor.grid(row=0, column=0)

        labelColorDisplay = Label(vehicleFrame, background=self.colors[i])
        labelColorDisplay.grid(row=0, column=1, sticky="ew")

        labelSpeed = Label(vehicleFrame, text="Speed")
        labelSpeed.grid(row=1, column=0)

        labelCurrentSpeed = Label(vehicleFrame, textvariable=speed)
        labelCurrentSpeed.grid(row=1, column=1)

        entryNewSpeed = Entry(vehicleFrame, textvariable=newSpeed)
        entryNewSpeed.grid(row=1, column=2)

        labelDistance = Label(vehicleFrame, text="Distance")
        labelDistance.grid(row=2, column=0)

        scaleDistance = Scale(vehicleFrame, from_=2, to=5, orient=HORIZONTAL)
        scaleDistance.grid(row=2, column=1)

        labelBattery = Label(vehicleFrame, text="Battery")
        labelBattery.grid(row=3, column=0)

        style = Style()
        style.theme_use("alt")
        style.configure("green.Horizontal.TProgressbar",
                        foreground="green", background="#5BC236")
        batteryLevel = Progressbar(
            vehicleFrame, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, mode="determinate")
        batteryLevel.grid(row=3, column=1, columnspan=2, sticky="ew")

        labelMacAdress = Label(vehicleFrame, text="Mac")
        labelMacAdress.grid(row=4, column=0)

        labelCurrentMac = Label(vehicleFrame, text=mac)
        labelCurrentMac.grid(row=4, column=1, columnspan=2, sticky="ew")

        # add padding
        for child in vehicleFrame.winfo_children():
            child.grid_configure(padx=10, pady=5)

        # Dict for accessing values
        values = {"speed": speed, "newspeed": newSpeed,
                  "distance": scaleDistance}

        return values

    def createVehicle(self, mac):
        index = len(self.vehicles)
        color = self.colors[index]
        position = 0

        vehicleEntry= {"number": index ,"mac": mac,"frame": self.createVehicleFrame(mac), "circle": self.createCircle(color),"color" : color,"positionIndex": position }
        self.vehicles.append(vehicleEntry)

        # todo create vehicle on server
        self.coordinator.createVehicle(mac)

    def createCircle(self, color):
        circle = self.mapCanvas.create_oval(0, 0, 0, 0, fill=color)
        return circle

    # replaces the old instnace in order to show on top of the canvas and be visible
    def fixCircles(self):
        for vehicle in self.vehicles:
            # remove old circle
            oldCircle = vehicle["circle"]
            self.mapCanvas.delete(oldCircle)

            newCircle = self.createCircle(vehicle["color"])
            vehicle["circle"] = newCircle

    def moveCircle(self, circle, x, y):
        newCoords = [x-self.radius, y-self.radius,
                     x+self.radius, y+self.radius]
        self.mapCanvas.coords(circle, newCoords)

    
                

    def sendValues(self):
        for lv in self.vehicles:
            vehicleMac = lv["mac"]
            vehicleFrame = lv["frame"]
            distance = ((vehicleFrame["distance"]).get())
            newspeed = ((vehicleFrame["newspeed"]).get())
            speed = ((vehicleFrame["speed"]).get())
            for ev in self.coordinator.vehicleList:
                if ev.addr == vehicleMac:
                    self.coordinator.setVehicleDistance(int(distance), vehicleMac)
                    self.coordinator.setVehicleSpeed(int(newspeed), vehicleMac)
        

    # This method gets called if there is an update of the vehicle values
    @staticmethod
    def batteryLevelUpdated(self, macAddress, batteryLevel):
        return

    # This method gets called if there is an update of the vehicle values
    @staticmethod
    def locationPositionUpdated(self, macAddress, location, piece, offset, speed, clockwiseVal):
        return

    # This method gets called if there is an update of the vehicle values
    @staticmethod
    def transitionUpdated(self, macAddress, piece, piecePrev, offset, direction, leftWheelDistance, rightWheelDistance):
        return


# Use with mac speed and x,y in canvas coordinates
def updateVehicles(gui):
    global update
    update = True
    while update:
        speeds = {}
        for v_c in gui.coordinator.vehicleList:
            speeds[v_c.addr] = v_c.speed

        for v in gui.vehicles:
            vehicleMac = v["mac"]
            # update ui display
            frame = v["frame"]           
            speed = speeds[vehicleMac]
            frame["speed"].set(speed)
            
            positionIndex = 0

            i = 0
            for pos in gui.coordinator.trackList.keys():
                if gui.coordinator.trackList[pos] == vehicleMac:
                    positionIndex = i - 1
                    break
                i += 1        

        #positionIndex = vehicleMac["position"]
        #positionIndex +=1
        #if positionIndex >len(self.list_canvas_checkpoints):
        #    positionIndex=0
        # update canvas
            if len(gui.list_canvas_checkpoints) > 0:
                print("Position für Punkt zeichnen {0}, {1}".format(gui.list_canvas_checkpoints[positionIndex][0], gui.list_canvas_checkpoints[positionIndex][1]))
                gui.moveCircle(v["circle"], gui.list_canvas_checkpoints[positionIndex][0], gui.list_canvas_checkpoints[positionIndex][1])
        time.sleep(0.1)


g = Gui(root)
root.mainloop()
os._exit(0)
