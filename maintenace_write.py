import socket
import struct

UDP_IP = "10.0.0.150" # SmartScan IP
UDP_PORT = 30070 # Maintenace message port

start = struct.pack(">IBBBBHBBHBBBBBB", 0xAA55E00E, 0, 0, 4, 2, 1, 3, 2, 5, 1, 1, 2, 0, 0, 0xFF) # start data transmission
stop = struct.pack(">IBBBBHBBHBBBBBB", 0xAA55E00E, 0, 0, 4, 2, 0, 3, 2, 0, 1, 1, 2, 0, 0, 0xFF) # stop data transmission
MESSAGE = stop

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))