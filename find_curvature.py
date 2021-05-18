import socket
import struct
import numpy as np
from scipy import constants
import sympy as sym

strain_free_wvs = np.load('C:\\fbg_data\\no_strain.npy')
params = np.load('C:\\fbg_data\\params.npy')

def process_peak(peak, start_f, step_f):
    if peak == 0:
        return 0
    ch = peak/128.  # Gives channel number
    freq = (start_f*1000 + step_f*ch) * 10e9   # frequency of the grating in Hz
    wl = constants.c/freq * 10e9  # convert to wavelength in nm
    return round(wl, 2)

def find_curvature(strains, parameters=None, n_gratings=16):

    if parameters is None:
        # Assume equal angles and radii for all gratings
        parameters = n_gratings * [[2*np.pi/3, 2*np.pi/3, 2.125, 2.125, 2.125]] # [angle between 1 and 2, angle between 1 and 3, S * radius 1, S * radius2, S * radius 3]
        parameters = np.array(parameters)

    # Find curvature
    curvs = np.empty(n_gratings, 3, 1)
    for ix, gt in enumerate(strains):
        strain_1 = gt[0]
        strain_2 = gt[1]
        strain_3 = gt[2]
        params = parameters[ix]
        u = solve_strain_eqs(strain_1, strain_2, strain_3, params)
        curvs[i] = u
    return curvs


def solve_strain_eqs(str1, str2, str3, params):
    # str1 - bias = -S * r1 * k * cos(theta)
    # str2 - bias = -S * r2 * k * cos(theta + alpha12)
    # str3 - bias = -S * r3 * k * cos(theta + alpha13)
    # Let u1 = k * cos(theta)
    #     u2 = k * sin(theta)
    # Then
    # str1 - bias + S * r1 * u1 = 0
    # str2 - bias + S * r2 * (u1 * cos(alpha12) - u2 * sin(alpha12)
    # str3 - bias + S * r3 * (u1 * cos(alpha13) - u2 * sin(alpha13)

    alpha12 = params[0]
    alpha13 = params[1]
    S_r1 = params[2]
    S_r2 = params[3]
    S_r3 = params[4]
    # Define symbols
    bias = sym.Symbol('bias')
    u1 = sym.Symbol('u1')
    u2 = sym.Symbol('u2')
    # solve linearly
    solution = sym.solve((str1 - bias + S_r1 * u1,
                          str2 - bias + S_r2 * (u1 * np.cos(alpha12) - u2 * np.sin(alpha12)),
                          str3 - bias + S_r3 * (u1 * np.cos(alpha13) - u2 * np.sin(alpha13))),
                         (bias, u1, u2))
    return np.array([u1, u2, 0]).reshape(3,1)



UDP_IP = "0.0.0.0" # PC IP
UDP_PORT = 30002 # Peak data port

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
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
        channels[:, i] = peaks[i * 16:(i + 1) * 16]

    # Check for any merged peaks (if less than 16 peaks are detected, some values will be 0)
    if np.any(channels == 0.0):
        continue

    # Find strains
    strains = np.log(channels / strain_free_wvs)

    # Find curvature
    curvatures = find_curvature(strains, params)
    print(curvatures)

    break