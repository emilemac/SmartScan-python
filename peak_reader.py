import socket
import struct

UDP_IP = "0.0.0.0" # PC IP
UDP_PORT = 30002 # Peak data port

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

c = True
while c == True:
    raw_data, addr = sock.recvfrom(2048)  # buffer size is 2048 bytes

    header = struct.unpack('>HBBIIIIHHHHII', raw_data[0:36])
    print("# total bytes:", header[0] + 2)
    print("# header bytes:", header[1] * 4)
    print("Frame format:", header[2])
    print("Incremented frame count:", header[3])
    print("Time Interval (micro s):", header[7])
    print("Min channel:", header[9])
    print("Max channel:", header[10])
    print("Start frequency (THz):", (header[11] >> 16) + ((header[11] & 0xFFFF) / 1000))
    print("Step frequency (GHz):", (header[12] >> 16) + ((header[12] & 0xFFFF) / 1000))

    data = struct.unpack('>' + 'H' * 704, raw_data[36:1444])
    print("Peaks:", data)

    c = False