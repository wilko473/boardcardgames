""" Graph generator
Generates a graph with the results of tournament values.
The values resulted from evaluate_keezen_rb.py"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from collections import OrderedDict

processed = OrderedDict()
processed['0'] = '0.002'
processed['503616000'] = '0.04075'
processed['1000435200'] = '0.09625'
processed['1503744000'] = '0.14925'
processed['2002457600'] = '0.192'
processed['2502784000'] = '0.235'
processed['3002022400'] = '0.24825'
processed['3503321600'] = '0.27475'
processed['4096486400'] = '0.32375'
processed['4512537600'] = '0.3375'
processed['5009305600'] = '0.3595'
processed['5502937600'] = '0.36275'
processed['6014822400'] = '0.37975'
processed['6506547200'] = '0.400'
processed['7016000000'] = '0.41275'
processed['7508390400'] = '0.42675'
processed['8001408000'] = '0.448'
processed['8519193600'] = '0.461'
processed['9018214400'] = '0.471'
processed['9516544000'] = '0.477'
processed['10014924800'] = '0.4845'
processed['10512601600'] = '0.497'

frames = list(dict.fromkeys(processed))
frames.sort(key=int, reverse=False)

values = list()
for frame in frames:
    values.append(float(processed[frame]) * 100)
frames_float = [float(i) for i in frames]
fig, ax = plt.subplots()

plt.title('Performance of DMC against rule-based agents', fontsize=14)
plt.xlabel('Number of frames trained', fontsize=14)
plt.ylabel('Win rate (%)', fontsize=14)

ax.plot(frames_float, values)
ax.xaxis.set_major_locator(MultipleLocator(1000000000))
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.set_ylim([0, 55])

plt.grid(True)
plt.plot()
plt.show()



