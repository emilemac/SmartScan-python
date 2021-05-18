import socket
import struct
import numpy as np
from scipy import constants

def process_peak(peak, start_f, step_f):
    if peak == 0:
        return 0
    ch = peak/128.  # Gives channel number
    freq = (start_f*1000 + step_f*ch) * 10e9   # frequency of the grating in Hz
    wl = constants.c/freq * 10e9  # convert to wavelength in nm
    return round(wl, 2)


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
    start_freq = (header[11] >> 16) + ((header[11] & 0xFFFF) / 1000)
    step_freq = (header[12] >> 16) + ((header[12] & 0xFFFF) / 1000)
    print("Start frequency (THz):", start_freq)
    print("Step frequency (GHz):", step_freq)

    data = struct.unpack('>' + 'H' * 704, raw_data[36:1444])
    peaks = tuple(map(lambda x: process_peak(x, start_freq, step_freq), data))
    print("Peaks:", list(peaks))

    c = False