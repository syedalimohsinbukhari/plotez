"""Created on Feb 27 11:03:47 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

rng = np.random.default_rng(91418482)

# Generate sample data with errors
x = np.linspace(0, 10, 20)
y = np.sin(x)
x_err = 0.25 * rng.random(len(x))
y_err = 0.3 * rng.random(len(y))

# Simple error bar plot
plot_errorbar(x, y, x_err=x_err, y_err=y_err)

# With custom styling
ep_config = ErrorPlotConfig(
    # Line styling
    linestyle="-",
    linewidth=2,
    color="darkblue",
    marker="o",
    markersize=6,
    alpha=0.7,
    # Error bar specific styling
    capsize=8,  # Length of error bar caps
    elinewidth=2,  # Width of error bar lines
    ecolor="red",  # Color of error bars (can differ from line color)
    capthick=2,  # Thickness of error bar caps
)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep_config, auto_label=True)

# plt.show()
plt.savefig("./images/QUICKSTART_style_errorbar.png", dpi=300)
plt.close()
