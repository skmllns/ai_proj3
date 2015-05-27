import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.axis([0, 100, 0, 100])
plt.ion()
plt.show()

for time.sleep(0.5)i in range(50):
    y = np.random.random()
    plt.scatter(i, y)
    plt.draw()
