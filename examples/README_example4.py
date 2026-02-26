"""Created on Feb 16 16:02:27 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

rng = np.random.default_rng(123)

x = np.linspace(0, 10, 16)
x_err = 0.25
y = np.sin(x)
y_err = abs(rng.normal(0, 0.25, (2, y.size)))  # Random errors for y

# Enhanced error bar styling
ep = ErrorPlotConfig(
    ecolor="red", capsize=8, color="darkblue", markerfacecolor="cyan", markeredgecolor="k", marker="o", linewidth=2
)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, auto_label=True, errorbar_config=ep, data_label=r"$\sin(x)$")

# plt.show()
plt.savefig("./images/README_example4.png", dpi=300)
plt.close()
