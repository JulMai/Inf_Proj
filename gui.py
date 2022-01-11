from tkinter import *
from tkinter.ttk import*
import threading
from tkinter.messagebox import askyesno
import mapping as mp
root = Tk()
root.title("Anki-Overdrive-Project")
#root.geometry("400x400")

class Gui:

    #Used to seperate the vehicles
    colors = ["green","blue","red","purple","yellow"]
    #radius for vehiclesCircles
    radius=10
    trackCoordinates=[]
    vehicles =[]
 
    def __init__(self,master):
        mainFrame = Frame(master)
        mainFrame.pack()
        
        #Canvas for Track
        self.mapCanvas = Canvas(mainFrame)
        self.mapCanvas.grid(row=0,column=0)
        #Sidebar for Vehicledata and Settings Choices
        self.settingsFrame = Frame(mainFrame)
        self.settingsFrame.grid(row=0,column=1,sticky="n")
        
        #all Vehicle Frame
        self.vehicleDataFrame = Frame (self.settingsFrame)
        self.vehicleDataFrame.grid(row=0,column=0)
        
        #settings like mode, scantrack etc
        self.generalSettingsFrame = Frame(self.settingsFrame)
        self.generalSettingsFrame.grid(row=1,column=0)

        #Thread Version only works once
        #self.scanTrackButton = Button(self.generalSettingsFrame, text="Scan Track", command=threading.Thread(target=self.scanTrack).start)
        
        #noThread Version
        self.scanTrackButton = Button(self.generalSettingsFrame, text="Scan Track", command=self.scanTrack)
        self.scanTrackButton.grid(row=0,column=4)       
    
        self.updateVehicleButton = Button(self.generalSettingsFrame, text="Update", command=self.sendValues)
        self.updateVehicleButton.grid(row=0,column=3)
        
        self.startButton = Button(self.generalSettingsFrame,text="Start",command=self.startSimulation)
        self.startButton.grid(row=0,column=0)
        
        self.stopButton = Button(self.generalSettingsFrame,text = "Stop", command=self.stopSimulation)
        self.stopButton.grid(row=0,column=2,padx=(0,20))
        
        for child in self.generalSettingsFrame.winfo_children():
            child.grid_configure(pady=5)
        #Testing
        self.createVehicle("111111")
        self.createVehicle("Berta")
        self.createVehicle("testo")
        
        
        
        #how to movecircle 2 forexample
        self.updateVehicle("testo",500,300,200)
     
    def startSimulation(self):
        answer = askyesno(title="Confirmation", message="Confirm that all vehicles are placed on the track!")
        
        if answer:
            #startSimutlation
            pass
        
     
    def stopSimulation(self):
        pass
        
    def scanTrack(self):
        #todo send msg to scan the track
        #get name of png
        
        self.trackImage = PhotoImage(file = r"C:\Users\andre\Downloads\track.png")
        self.mapCanvas.config(width = self.trackImage.width(), height = self.trackImage.height())       
        self.mapCanvas.create_image(0,0,image=self.trackImage,anchor="nw")
        self.trackCoordinates = mp.map_grid()
        
        self.fixCircles()
        
    
    def createVehicleFrame(self,mac):
        frame = self.vehicleDataFrame
        
        #init Variables for Display
        speed=StringVar()
        newSpeed=StringVar()
        distance=StringVar()
        macAdress=StringVar()
        macAdress.set(mac)
        
        
        i=len(self.vehicles)       
        vehicleFrame = LabelFrame(frame, text=i)
        vehicleFrame.grid(row=i,column=0)
        
            
        labelColor = Label(vehicleFrame, text="Color")
        labelColor.grid(row=0,column=0)
            
        labelColorDisplay= Label(vehicleFrame, background=self.colors[i])
        labelColorDisplay.grid(row=0, column=1, sticky="ew")
        
        labelSpeed= Label(vehicleFrame,text="Speed")
        labelSpeed.grid(row=1, column=0)
        
        labelCurrentSpeed = Label(vehicleFrame, textvariable=speed)
        labelCurrentSpeed.grid(row=1, column=1)
        
        entryNewSpeed = Entry(vehicleFrame,textvariable=newSpeed)
        entryNewSpeed.grid(row=1,column=2)
        
        labelDistance = Label(vehicleFrame,text="Distance")
        labelDistance.grid(row=2, column=0)
        
        scaleDistance = Scale(vehicleFrame, from_=1,to=5,orient=HORIZONTAL)
        scaleDistance.grid(row=2,column=1)
        
        labelBattery = Label(vehicleFrame,text="Battery")
        labelBattery.grid(row=3, column=0)
        
        style= Style()
        style.theme_use("alt")
        style.configure("green.Horizontal.TProgressbar",foreground="green",background="#5BC236")
        batteryLevel = Progressbar(vehicleFrame,style="green.Horizontal.TProgressbar",orient=HORIZONTAL,mode="determinate")
        batteryLevel.grid(row=3,column=1,columnspan=2,sticky="ew")
 
        labelMacAdress= Label(vehicleFrame, text="Mac")
        labelMacAdress.grid(row=4, column=0)
        
        labelCurrentMac= Label(vehicleFrame,text=mac)
        labelCurrentMac.grid(row=4, column=1,columnspan=2,sticky="ew")
        
        #add padding
        for child in vehicleFrame.winfo_children():
            child.grid_configure(padx=10,pady=5)
              
        
        #Dict for accessing values
        values = {"speed": speed,"newspeed":newSpeed,"distance": scaleDistance}
        
        return values
           
    def createVehicle(self,mac):
        index = len(self.vehicles)
        color = self.colors[index]
        position = 0
        
        vehicleEntry= {"number": index ,"mac": mac,"frame": self.createVehicleFrame(mac), "circle": self.createCircle(color),"color" : color,"positionIndex": position }
        self.vehicles.append(vehicleEntry)
        
        #todo create vehicle on server 
    
    def createCircle(self,color):
        circle= self.mapCanvas.create_oval(0,0,0,0,fill=color)
        return circle
        
    #replaces the old instnace in order to show on top of the canvas and be visible
    def fixCircles(self):
        for vehicle in self.vehicles:
            #remove old circle
            oldCircle = vehicle["circle"]
            self.mapCanvas.delete(oldCircle)
            
            newCircle = self.createCircle(vehicle["color"])
            vehicle["circle"] = newCircle
    
    def moveCircle(self, circle, x, y):
        newCoords=[x-self.radius, y-self.radius, x+self.radius, y+self.radius]
        self.mapCanvas.coords(circle,newCoords)
    
    
    #Use with mac speed and x,y in canvas coordinates      
    def updateVehicle(self,mac,speed,x,y):
        for v in self.vehicles:
            vehicleMac = v["mac"]
            if vehicleMac == mac:
                #update ui display
                frame = v["frame"]
                frame["speed"].set(speed)
                

                #assumes callback everytime new checkpoint is entered
                positionIndex = vehicleMac["position"]
                positionIndex +=1
                if positionIndex >len(self.trackCoordinates):
                    positionIndex=0
                #update canvas
                self.moveCircle(v["circle"],self.trackCoordinates[positionIndex]) 
        
    
    def sendValues(self):
        for v in self.vehicles:
            vehicleFrame= v["frame"]
            distance = ((vehicleFrame["distance"]).get())
            newspeed = ((vehicleFrame["newspeed"]).get())
            speed = ((vehicleFrame["speed"]).get())
            
            #If no entry do nothing       
            
        
      
g = Gui(root)
root.mainloop()

        