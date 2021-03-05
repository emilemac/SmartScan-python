import socket
import struct
from datetime import datetime

current_time = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()

UDP_IP = "10.0.0.150" # SmartScan IP
UDP_PORT = 30001 # Diagnostic message port

# Message contents:
#     u(32) uITimeStamp
#     u(8)  ucDamage (not used)
#     u(8)  ucState (0 = No Change, 1 = STANDBY, 2 = OPERATIONAL, 3 = MAINTENANCE)
#     u(8)  ucvLevel1damage[8] (not used)
#     u(8)  ucvLevel2damage[8] (not used)
#     u(8)  ucvSpare[8] (not used)
MESSAGE = struct.pack("IBBBBB", int(current_time), 0, 2, 0, 0, 0)

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))