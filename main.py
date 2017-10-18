import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

path = 'Data/No_mass'
#path = 'Data/Mass'

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

peaks = []

for i in range(max_detection_window, len(average) - max_detection_window):
    if average[i] == max(average[i - max_detection_window: i + max_detection_window]):
        peaks.append((time_stamp[i], average[i]))


plt.plot(time_stamp, average, color='r')

for peak in peaks:
    plt.plot(peak[0], peak[1], "*", color='b')

dt = []

for i in range(1, len(peaks)):
    dt.append(peaks[i][0] - peaks[i - 1][0])

dt = sum(dt) / len(dt)

print(dt)

plt.show()

