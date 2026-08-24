"""Created on Aug 24, 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import BarPlotConfig, SAVE_DPI, plot_bar

categories = ["A", "B", "C", "D", "E"]
values = np.array([23, 45, 12, 39, 28])

b_cfg = BarPlotConfig(color="steelblue", edgecolor="black", alpha=0.85)
plot_bar(categories, values, x_label="Category", y_label="Value", plot_title="Bar Plot", bar_config=b_cfg)

# plt.show()
plt.savefig("README_E9_bar_plot.png", dpi=SAVE_DPI)
plt.close()
