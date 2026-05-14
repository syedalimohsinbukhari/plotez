"""Created on Mar 08 02:41:05 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

x = np.linspace(0, 10, 100)
y = np.sin(x)

plot_xy(
    x_data=x,
    y_data=y,
    x_label="Time (s)",
    y_label="Amplitude (V)",
    data_label="Channel A",
    plot_title="Sinusoidal Signal",
)

# plt.show()
plt.savefig("RTD_E2_custom_labels.png", dpi=300)
plt.close()
