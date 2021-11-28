from vehicle.overdrive import Overdrive
import struct
import threading
import queue
import logging
import bluepy.btle as btle


class Vehicle(Overdrive):

    def __init__(self, vehicleMacAddress):
        #Overdrive.__init__(self, vehicleMacAddress)
        print("constructor of Vehicle called")
        self.addr = vehicleMacAddress
        self._peripheral = btle.Peripheral()
        self._readChar = None
        self._writeChar = None
        self._connected = False
        self._reconnect = False
        self._delegate = OverdriveDelegateNew(self)
        self._writeQueue = queue.Queue()
        self._btleSubThread = None
        self.speed = 0
        self.desired_speed = 0
        self.location = 0
        self.piece = 0
        self.batteryStatus = -1
        self.acceleration = 0
        self.clockwise = False  # !not final, waiting for validation
        self.direction = 0  # !not final, waiting for validation
        self.offset = 0  # !not final, waiting for validation
        self.piecePrev = 0  # !not final, waiting for validation
        self.abstand = 0
        # Setter function !not final, only for testing
        #self._locationChangeCallbackFunc = lambda location, piece, offset, speed, clockwiseVal: self.location=location, self.piece=piece, self.offset=offset, self.speed=speed
        self._locationChangeCallbackFunc = None
        self._pongCallbackFunc = None  # todo
        # Setter function !not final, only for testing
        #self._transitionCallbackFunc = lambda piece, piecePrev, offset, direction: self.piece=piece, self.piecePrev=piecePrev, self.offset=offset, self.direction=direction
        self._transitionCallbackFunc = None
        while True:
            try:
                self.connect()
                break
            except btle.BTLEException as e:
                logging.getLogger("anki.overdrive_t1").error(e.message)

    def test_version(self ):
        self.sendCommand(struct.pack("<B", "0x18"))

    def changeSpeed(self, speed, accel):
        self.speed = speed
        self.acceleration = accel
        command = struct.pack("<BHHB", 0x24, speed, accel, 0x01)
        self.sendCommand(command)

    def changeLaneRight(self, speed, accel):
        self.speed = speed
        self.acceleration = accel
        self.changeLane(speed, accel, 44.5)

    def changeLaneLeft(self, speed, accel):
        self.speed = speed
        self.acceleration = accel
        self.changeLane(speed, accel, -44.5)

    def makeUTurn(self):
        # u-turn command
        command = struct.pack("<BBB", 0x32, 3, 0)
        self.sendCommand(command)

    def sendBatteryStatusRequest(self):
        # battery level request command
        command = struct.pack("<B", 0x1a)
        self.sendCommand(command)

    def _setBatteryStatus(self, batteryStatus):
        self.batteryStatus = batteryStatus

    def getBatteryStatus(self):
        if self.batteryStatus > -1:
            return self.batteryStatus


class OverdriveDelegateNew:
    sum_left = 0
    sum_right = 0
    def __init__(self, vehicle):
        self.handle = None
        self.notificationsRecvd = 0
        self.vehicle = vehicle
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):
        if self.handle == handle:
            self.notificationsRecvd += 1
            (commandId,) = struct.unpack_from("B", data, 1)
            if commandId == 0x1b:
                # Battery status response
                threading.Thread(target=self.vehicle._setBatteryStatus, args=(
                    struct.unpack_from("<B", data, 2))).start()
            if commandId == 0x27:
                # Location position
                location, piece, offset, speed, clockwiseVal = struct.unpack_from(
                    "<BBfHB", data, 2)
                clockwise = False
                #print(struct.unpack_from("<BBfHBBBHH", data, 2))
                if clockwiseVal == 0x47:
                    clockwise = True
                threading.Thread(target=self.vehicle._locationChangeCallback, args=(
                    location, piece, speed, clockwise)).start()
            if commandId == 0x19:
                #print(struct.unpack_from(data, 2))
                pass
            if commandId == 0x29:
                # Transition notification
                #piece, piecePrev, offset, direction = 

                self.sum_left = self.sum_left + int(struct.unpack_from("<B", data, 16)[0])
                self.sum_right = self.sum_right + int(struct.unpack_from("<B", data, 17)[0])
                #print(struct.unpack_from("<fBBHbBBBBB", data, 4))
                threading.Thread(
                    target=self.vehicle._transitionCallback).start()
            elif commandId == 0x17:
                # Pong
                threading.Thread(target=self.vehicle._pongCallback).start()
            

    def setHandle(self, handle):
        self.handle = handle
        self.notificationsRecvd = 0
