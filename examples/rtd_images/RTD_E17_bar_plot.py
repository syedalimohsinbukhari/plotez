"""Created on Aug 24, 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import BarPlotConfig, SAVE_DPI, plot_bar, plot_barh

categories = ["A", "B", "C", "D", "E"]
values = np.array([23, 45, 12, 39, 28])

b_cfg = BarPlotConfig(color="steelblue", edgecolor="black", alpha=0.85)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

plot_bar(categories, values, x_label="Category", y_label="Value", plot_title="Bar Plot", bar_config=b_cfg, axis=ax1)
plot_barh(
    categories,
    values,
    x_label="Category",
    y_label="Value",
    plot_title="Horizontal Bar Plot",
    bar_config=b_cfg,
    axis=ax2,
)

plt.tight_layout()

# plt.show()
plt.savefig("RTD_E17_bar_plot.png", dpi=SAVE_DPI)
plt.close()
