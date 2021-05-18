import socket
import struct
import numpy as np
from scipy import constants

strain_free_wvs = np.load('C:\\fbg_data\\no_strain.npy')

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

strain_arr = []
full_arr = []
try:
    while True:
        raw_data, addr = sock.recvfrom(2048)  # buffer size is 2048 bytes

        header = struct.unpack('>HBBIIIIHHHHII', raw_data[0:36])
        start_freq = (header[11] >> 16) + ((header[11] & 0xFFFF) / 1000)
        step_freq = (header[12] >> 16) + ((header[12] & 0xFFFF) / 1000)

        data = struct.unpack('>' + 'H' * 704, raw_data[36:1444])
        peaks = tuple(map(lambda x: process_peak(x, start_freq, step_freq), data))

        # Split into channels
        peaks = list(peaks)
        channels = np.zeros((16, 3))
        for i in range(3):
            channels[:, i] = peaks[i * 16:(i + 1) * 16]

        # Find strains
        strains = np.log(channels/strain_free_wvs)
        full_arr.append(strains)

        # Check for any merged peaks (if less than 16 peaks are detected, some values will be 0)
        if np.any(channels == 0.0):
            continue

        strain_arr.append(strains)

        #break

except KeyboardInterrupt:
    pass

# Choose a range of gratings, e.g. 12 to 16 will calibrate the last four gratings 13, 14, 15, 16.
begin = 4
end = 7
name = str(begin) + "_" + str(end)
# Choose the radius of curvature used in mm
curv_radius = 750
# Save recorded strains
strain_arr = np.array(strain_arr)
np.save('C:\\fbg_data\\calib_strains_' + name + '_' + str(curv_radius) + '.npy', strain_arr) # all 16 x 3 grating strains will be saved
np.save('C:\\fbg_data\\full_calib_strains_' + name + '_' + str(curv_radius) + '.npy', np.array(full_arr)) # save with noise
print(len(strain_arr))