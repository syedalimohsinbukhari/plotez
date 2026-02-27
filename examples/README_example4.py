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
errorbar_config = ErrorPlotConfig(
    color="darkblue",
    linewidth=2,
    alpha=0.25,
    ecolor="red",
    marker="o",
    markerfacecolor="cyan",
    markeredgecolor="k",
    capsize=8,
)

plot_errorbar(
    x_data=x,
    y_data=y,
    x_err=x_err,
    y_err=y_err,
    auto_label=True,
    errorbar_config=errorbar_config,
    data_label=r"$\sin(x)$",
)

# plt.show()
plt.savefig("./images/README_example4.png", dpi=300)
plt.close()
