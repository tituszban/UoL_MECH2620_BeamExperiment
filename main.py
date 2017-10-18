import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import math

def detect_peaks(data, time_stamp):
    peaks_mx = []
    peaks_mn = []

    for i in range(max_detection_window, len(data) - max_detection_window):
        if average[i] == max(data[i - max_detection_window: i + max_detection_window]):
            peaks_mx.append((time_stamp[i], data[i]))
        if average[i] == min(data[i - max_detection_window: i + max_detection_window]):
            peaks_mn.append((time_stamp[i], data[i]))

    return peaks_mx, peaks_mn


def calculate_dt(peaks_mx, peaks_mn):
    dt = []

    for i in range(1, len(peaks_mx)):
        dt.append(peaks_mx[i][0] - peaks_mx[i - 1][0])
    for i in range(1, len(peaks_mn)):
        dt.append(peaks_mn[i][0] - peaks_mn[i - 1][0])

    return sum(dt) / len(dt)


def calculate_error_offset(peaks_mx, peaks_mn):

    sum = 0
    counter = 0
    for peak_mx in peaks_mx:
        sum += peak_mx[1]
        counter += 1
    for peak_mn in peaks_mn:
        sum += peak_mn[1]
        counter += 1
    return sum / counter

    error_mn = []
    error_mx = []
    for i in range(1, len(peaks_mn)):
        ratio = math.sqrt(abs(peaks_mn[i - 1][1] / peaks_mn[i][1]))
        error_mn.append(ratio * abs(peaks_mn[i][1]) - peaks_mx[i - 1][1])

    for i in range(1, len(peaks_mx)):
        ratio = math.sqrt(abs(peaks_mx[i - 1][1] / peaks_mx[i][1]))
        error_mx.append(ratio * peaks_mx[i][1] - abs(peaks_mx[i][1]))

    return -(sum(error_mn) / len(error_mn) - sum(error_mx) / len(error_mx)) / 2

def square_error(data1, data2):
    error = 0
    if len(data1) != len(data2):
        raise "Error"
    for i, _ in enumerate(data1):
        error += (data1[i] - data2[i]) ** 2
    return error

path = 'Data/No_mass'
path = 'Data/Mass'

data = []
time_stamp = []

TIME_RANGE = 400

max_detection_window = 5

files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

for file in files:
    with open(file, 'r') as text:
        single_data = []
        for line in text:
            try:
                single_data.append(float(line.split(',')[1]))
            except: pass
        # data.append([float(line.split(',')[1]) for line in text[1:]])
        data.append(single_data)

with open(files[0], 'r') as text:
    for line in text:
        try:
            time_stamp.append(float(line.split(',')[0]))
        except:
            pass

data = np.array(data)
time_stamp = np.array(time_stamp)

average = [ sum(data[:, i]) / data.shape[0] for i in range(data.shape[1])]
average = np.array(average)[:TIME_RANGE]

time_stamp = time_stamp[:TIME_RANGE]

#for dat in data:
    #plt.plot(time_stamp, dat[:TIME_RANGE])

peaks_mx, peaks_mn = detect_peaks(average, time_stamp)



dt = calculate_dt(peaks_mx, peaks_mn)

print('dt:', dt)


error_offset = calculate_error_offset(peaks_mx, peaks_mn)
print('initial error:', error_offset)
average = average - error_offset

peaks_mx, peaks_mn = detect_peaks(average, time_stamp)


error_offset = calculate_error_offset(peaks_mx, peaks_mn)
print('adjusted error:', error_offset)

plt.plot(time_stamp, average, color='r')
for peak in peaks_mx:
    plt.plot(peak[0], peak[1], "*", color='b')
for peak in peaks_mn:
    plt.plot(peak[0], peak[1], '*', color='g')

print([peak[1] for peak in peaks_mx])
print([peak[1] for peak in peaks_mn])

sigma = []

for i in range(1, len(peaks_mx)):
    sigma.append(1 / i * math.log(abs(peaks_mx[0][1] / peaks_mx[i][1])))
for i in range(1, len(peaks_mn)):
    sigma.append(1 / i * math.log(abs(peaks_mn[0][1] / peaks_mn[i][1])))

print(sigma)

sigma = sum(sigma) / len(sigma)

print('log decrement:', sigma)

zeta = sigma / (2 * math.pi)
omega_d = 2 * math.pi / dt
omega_n = omega_d / math.sqrt(1 - (zeta ** 2))

print('omega_d:', omega_d)
print('omega_n:', omega_n)
print('zeta:', zeta)

SCALER_SWEEP_RANGE = (8, 12)
SCALER_SWEEP_STEP = 0.05

THETA_SWEEP_RANGE = (0, 6.28)
THETA_SWEEP_STEP = 0.1

min_error = 9999999999
best_scaler = 0
best_theta = 0

for i in range(math.floor(THETA_SWEEP_RANGE[1] / THETA_SWEEP_STEP)):
    for j in range(math.floor(SCALER_SWEEP_RANGE[1] / SCALER_SWEEP_STEP)):
        scaler = SCALER_SWEEP_RANGE[0] + SCALER_SWEEP_STEP * j
        theta = THETA_SWEEP_RANGE[0] + THETA_SWEEP_STEP * i

        reference = [scaler * math.exp(-omega_n * zeta * v) * math.sin(omega_d * v + theta) for v in time_stamp]

        error = square_error(average, reference)
        if error < min_error:
            min_error = error
            best_scaler = scaler
            best_theta = theta

print(best_theta, best_scaler)

reference = [best_scaler * math.exp(-omega_n * zeta * v) * math.sin(omega_d * v + best_theta) for v in time_stamp]

plt.plot(time_stamp, reference)
plt.plot(time_stamp, [0 for _ in time_stamp])

plt.show()

