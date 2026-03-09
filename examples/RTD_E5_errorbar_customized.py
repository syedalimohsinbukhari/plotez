"""Created on Mar 08 02:44:26 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

x = np.linspace(0, 10, 20)
y = np.sin(x)
y_err = 0.2

ep = ErrorPlotConfig(
    color="darkblue",  # Line and marker color
    linewidth=2,
    marker="o",
    markersize=6,
    capsize=5,
    ecolor="crimson",  # Error bar color (different!)
    elinewidth=1.5,
    markerfacecolor="gold",
)
plot_errorbar(
    x_data=x,
    y_data=y,
    y_err=y_err,
    x_label="X",
    y_label="Y",
    plot_title="Errorbar demonstration",
    data_label="Measurements",
    errorbar_config=ep,
)

# plt.show()
plt.savefig("./rtd_images/RTD_E5_errorbar_customized.png", dpi=300)
plt.close()
