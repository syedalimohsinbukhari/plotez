"""Created on Feb 16 11:28:34 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy
from plotez.backend.utilities import LinePlot

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create custom line plot parameters
line_params = LinePlot(
    line_style=['-'],
    line_width=[2],
    color=['#FF5733'],
    marker=['o'],
    marker_size=[4]
)

plot_xy(x, y, plot_dictionary=line_params)

# plt.show()
plt.savefig("./README_example4.png")
plt.close()
