"""Created on Mar 08 02:41:05 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

x = np.linspace(0, 10, 100)
y = np.sin(x)

plot_xy(x, y, x_label="Time (s)", y_label="Amplitude (V)", plot_title="Sinusoidal Signal", data_label="Channel A")

# plt.show()
plt.savefig("./rtd_images/RTD_E2_custom_labels.png", dpi=300)
plt.close()
