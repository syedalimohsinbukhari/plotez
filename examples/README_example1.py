"""Created on Feb 16 11:24:06 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot with automatic labeling
plot_xy(x, y, auto_label=True)
# plt.show()
plt.savefig("./images/README_example1.png")
plt.close()
