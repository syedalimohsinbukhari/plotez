"""Created on Mar 08 04:47:49 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar, plot_xy

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plotez on first subplot
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
plot_xy(x, y1, axis=ax1, x_label="X", y_label="Y", data_label="sin(x)")

# Plotez on second subplot
x2 = np.linspace(0, 10, 20)
y2 = np.cos(x2)
y_err = 0.1
plot_errorbar(x2, y2, y_err=y_err, axis=ax2, x_label="X", data_label="cos(x)")

# plt.show()
plt.savefig("./rtd_images/RTD_E12_matplotlib_integration.png", dpi=300)
plt.close()
