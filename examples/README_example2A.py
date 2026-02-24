"""Created on Feb 16 11:26:26 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xyy
from plotez.backend import LinePlot

x = np.linspace(0, 10, 50)
y1 = np.sin(x)
y2 = np.exp(-x / 10)

plot_config = LinePlot(
    line_style=["--", "-."],
    color=["red", "cyan"],
    marker=["o", "s"],
    marker_size=[10, 10],
    mark_every=[3, 5],
    marker_edge_color=["k", "k"],
)

plot_xyy(
    x,
    y1,
    y2,
    x_label="Time",
    y1_label="Sine",
    y2_label="Exponential",
    data_labels=["sin(x)", "exp(-x/10)"],
    plot_config=plot_config,
)

# plt.show()
plt.savefig("./images/README_example2A.png", dpi=300)
plt.close()
