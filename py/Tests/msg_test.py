import struct
from overdrive import Overdrive

car = Overdrive("EC:33:B4:DB:9E:C8")
cmd = struct.pack(1, 0x1a)
car.sendCommand(cmd)