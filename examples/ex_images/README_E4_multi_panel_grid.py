"""Created on Mar 08 02:15:02 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, n_plotter

x_data = [np.linspace(0, 10, 100) for _ in range(4)]
y_data = [np.sin(x_data[0]), np.cos(x_data[1]), np.tan(x_data[2] / 5), x_data[3] ** 2 / 100]

n_plotter(x_data, y_data, n_rows=2, n_cols=2, data_labels=["X1 vs Y1", "X2 vs Y2", "X3 vs Y3", "X4 vs Y4"])

# plt.show()
plt.savefig("README_E4_multi_panel_grid.png", dpi=SAVE_DPI)
plt.close()
