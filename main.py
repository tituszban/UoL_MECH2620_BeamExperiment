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

path = 'Data/No_mass'
path = 'Data/Mass'

data = []
time_stamp = []

TIME_RANGE = 500

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

for i in range(1, len(peaks_mx) - 3):
    sigma.append(1 / i * math.log(abs(peaks_mx[0][1] / peaks_mx[i][1])))
for i in range(1, len(peaks_mn) - 3):
    sigma.append(1 / i * math.log(abs(peaks_mn[0][1] / peaks_mn[i][1])))

sigma = sum(sigma) / len(sigma)

print('log decrement:', sigma)

zeta = sigma / (2 * math.pi)
omega_d = 2 * math.pi / dt
omega_n = omega_d / math.sqrt(1 - (zeta ** 2))

print('omega_d:', omega_d)
print('omega_n:', omega_n)
print('zeta:', zeta)

scaler = 9
theta = 4.2

reference = [scaler * math.exp(-omega_n * zeta * v) * math.sin(omega_d * v + theta) for v in time_stamp]

plt.plot(time_stamp, reference)
plt.plot(time_stamp, [0 for _ in time_stamp])

plt.show()

