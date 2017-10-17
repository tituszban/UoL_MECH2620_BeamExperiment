import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

path = 'Data/No_mass'

data = []
time_stamp = []

TIME_RANGE = 400

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

average = data.mean(0)[:TIME_RANGE]
time_stamp = time_stamp[:TIME_RANGE]

A = 0
A_sweep_range = [8, 20]
A_step = 0.1

Tau = 0
Tau_sweep_range = [0.1, 1]
Tau_step = 0.05

for dat in data:
    plt.plot(time_stamp, dat[:TIME_RANGE])

plt.plot(time_stamp, average)

plt.show()