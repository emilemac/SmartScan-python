import socket
import struct

UDP_IP = "0.0.0.0" # PC IP
UDP_PORT = 30001 # Diagnostic message port

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    message, addr = sock.recvfrom(2048)  # buffer size is 2048 bytes
    print(message) # Reply from SmartScan