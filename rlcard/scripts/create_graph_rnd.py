""" Renders the results of tournaments in a graph
Picks the last generated model and start a tournament against randomly playing agents.

"""
import csv
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


path = './experiments/dmc_keezen_result/keezenexpid8/'
processed = OrderedDict()
try:
    with open(path + 'processed.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        processed = OrderedDict(reader)
except IOError:
    print("File does not exist.")

frames = list(dict.fromkeys(processed))
frames.sort(key=int, reverse=False)

values = list()
for frame in frames:
    values.append(float(processed[frame]) * 100)
frames_float = [float(i) for i in frames]
fig, ax = plt.subplots()

plt.title('Performance of DMC against randomly playing agents', fontsize=14)
plt.xlabel('Number of frames trained', fontsize=14)
plt.ylabel('Win rate (%)', fontsize=14)

ax.plot(frames_float, values)
ax.xaxis.set_major_locator(MultipleLocator(500000000))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.set_ylim([50, 100])

plt.grid(True)
plt.plot()
plt.show()



