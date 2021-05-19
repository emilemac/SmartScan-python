import numpy as np
import os.path
from scipy import optimize
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


def cosine(x, a, b, c, d):
    y = a * np.cos(b * x + c) + d
    return y

def fit_cosine(strains):
    for i in range(3):
        x_data = np.linspace(0, len(strains) - 1, len(strains))
        y_data = strains[:, i]
        params, params_covariance = optimize.curve_fit(cosine, x_data, y_data)
        print(params)

        a = params[0]
        b = params[1]
        c = params[2]
        d = params[3]
        break

    plt.figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.title('Cosine Function Fit')
    plt.errorbar(x_data, y_data, fmt='o', marker='o', label='Strain', markersize=3, color='k', elinewidth=1,
                 capsize=2, markeredgewidth=1)
    plt.plot(x_data, cosine(x_data, a, b, c, d), label='Fitted cosine')
    plt.legend(loc='best')
    plt.ylabel('Strain')
    plt.xlabel('Time')
    plt.show()

def main():

    params = None
    if os.path.isfile('C:\\fbg_data\\params.npy'):
        params = np.load('C:\\fbg_data\\params.npy')
    else:
        # set to dummy values
        params = 16 * [[2 * np.pi / 3, 2 * np.pi / 3, 2.125, 2.125, 2.125]]  # [angle between 1 and 2, angle between 1 and 3, S * radius 1, S * radius2, S * radius 3]
        params = np.array(params)


    # Choose gratings to load, e.g. 12 to 16 will load data for the last four gratings 13, 14, 15, 16.
    begin = 4
    end = 7
    # Specify curvature radius used for calibration
    curv_rad = 750
    name = str(begin) + "_" + str(end) + '_' + str(curv_rad)
    # Load recorded strains
    #strains_160 = np.load('C:\\fbg_data\\calib_strains_' + name + '_160.npy')
    #strains_250 = np.load('C:\\fbg_data\\calib_strains_' + name + '_250.npy')
    #strains_400 = np.load('C:\\fbg_data\\calib_strains_' + name + '_400.npy')
    strains_750 = np.load('C:\\fbg_data\\calib_strains_' + name + '.npy')
    noisy_strains_750 = np.load('C:\\fbg_data\\full_calib_strains_' + name + '.npy')

    # Specify grating number (0-15)
    grating = 11

    # Smooth data
    window = 100
    smoothed = []
    for i in range(3):
        cumsum_vec = np.cumsum(np.insert(strains_750[:,grating,i], 0, 0))
        new_vec = (cumsum_vec[window:] - cumsum_vec[:-window]) / window
        smoothed.append(new_vec)
    smoothed = np.array(smoothed).T


    #cosine = fit_cosine(strains_750[:,grating,:])

    # Print highest and lowest strain values
    print("Ch 1 g " + str(grating) + " min:", np.min(smoothed[:,0]), " max:", np.max(smoothed[:,0]))
    #print("Ch 1 g " + str(grating) + " min:", np.min(strains_750[:, grating, 0]), " max:", np.max(strains_750[:, grating, 0]))
    print("\n")
    print("Ch 2 g " + str(grating) + " min:", np.min(smoothed[:, 1]), " max:", np.max(smoothed[:, 1]))
    #print("Ch 2 g " + str(grating) + " min:", np.min(strains_750[:, grating, 1]), " max:", np.max(strains_750[:, grating, 1]))
    print("\n")
    print("Ch 3 g " + str(grating) + " min:", np.min(smoothed[:, 2]), " max:", np.max(smoothed[:, 2]))
    #print("Ch 3 g " + str(grating) + " min:", np.min(strains_750[:, grating, 2]), " max:", np.max(strains_750[:, grating, 2]))

    # Plot strains
    ax = plt.figure()
    # plt.plot(strains_250[:,0,:])
    # plt.plot(strains_400[:,0,:])
    plt.plot(strains_750[:, grating, :])
    ax1 = plt.figure()
    # plt.plot(noisy_strains_750[:, 11, :])
    plt.plot(smoothed)
    plt.show()


    # Set angles to default 120 degrees
    params[grating, 0] = 2 * np.pi / 3
    params[grating, 1] = 2 * np.pi / 3
    # Set S*r values
    for i in range(3):
        amplitude = np.max(smoothed[:,i]) - np.min(smoothed[:,i])
        k = 1.0 / curv_rad  # curvature
        S_r = amplitude / (2 * k)
        params[grating, 2+i] = S_r

    # Save parameters
    np.save('C:\\fbg_data\\params.npy', params)
    print(params)


if __name__ == "__main__":
    main()