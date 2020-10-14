import matplotlib.pyplot as plt
import numpy as np

fig0 = plt.figure()  # an empty figure with no Axes
fig1, ax = plt.subplots()  # a figure with a single Axes
fig2, axs = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes


ax.plot([2,4,6,8],[2,4,6,8])
axs[0].plot([1, 2, 3, 4], [1, 4, 2, 3])

plt.show()


print(ax)
print(axs)