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
    return wl


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
    # Split into channels
    peaks = list(peaks)
    channels = np.zeros((16, 3))
    for i in range(3):
        # Take mean of 3 measurements and round to 2 decimal place
        channels[:, i] = list(map(lambda x: round(x,2), np.mean([peaks[i * 16:(i + 1) * 16], peaks[(i+4) * 16:(i + 5) * 16], peaks[(i+8) * 16:(i + 9) * 16]], axis=0)))
    # Save Bragg wavelengths
    np.save('C:\\fbg_data\\no_strain.npy', channels)
    print(channels)

    c = False