"""Created on Feb 16 16:02:27 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlot

rng = np.random.default_rng(123)

x = np.linspace(0, 10, 16)
x_err = 0.25
y = np.sin(x)
y_err = abs(rng.normal(0, 0.25, (2, y.size)))  # Random errors for y

# Enhanced error bar styling
ep = ErrorPlot(
    error_color="red",
    capsize=8,
    color="darkblue",
    marker_face_color="cyan",
    marker_edge_color="k",
    marker="o",
    line_width=2,
)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, auto_label=True, errorbar_config=ep, data_label=r"$\sin(x)$")

# plt.show()
plt.savefig("./images/README_example4.png", dpi=300)
plt.close()
