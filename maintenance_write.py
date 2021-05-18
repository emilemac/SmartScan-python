import socket
import struct

UDP_IP = "10.0.0.150" # SmartScan IP
UDP_PORT = 30070 # Maintenance message port

# Commands to start and stop data transmission
start = struct.pack(">IBBBBHBBHBBBBBB", 0xAA55E00E, 0, 0, 4, 2, 1, 3, 2, 5, 1, 1, 2, 0, 0, 0xFF)
stop = struct.pack(">IBBBBHBBHBBBBBB", 0xAA55E00E, 0, 0, 4, 2, 0, 3, 2, 0, 1, 1, 2, 0, 0, 0xFF)

# Set channel format:
# bits 0..3 indicate 4 channels (0100)
# bits 4..8 indicate 16 gratings (10000)
# bit 14 set to 1 to store peaks contiguously (not using slots)
# bit 15 set to 0 in order to choose # of channels and gratings
bits = 0b0100100000000010
bits = 0b0100000100000100
set_channel_format = struct.pack(">IBBBBHBB", 0xAA55E00E, 0, 0, 5, 2, bits, 0, 0xFF)

MESSAGE = stop

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))