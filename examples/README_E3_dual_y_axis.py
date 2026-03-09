"""Created on Mar 08 02:13:52 2026"""

import numpy as np
from matplotlib import pyplot as plt

from plotez import plot_xyy

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(-x / 10)

plot_xyy(
    x, y1, y2, x_label="Time (s)", y1_label="Signal (V)", y2_label="Decay", data_labels=["Oscillation", "Envelope"]
)

# plt.show()
plt.savefig("./ex_images/README_E3_dual_y_axis.png", dpi=300)
plt.close()
