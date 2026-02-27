"""Created on Feb 26 09:52:15 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez.backend import ErrorBandConfig, LinePlotConfig
from plotez.plotez import plot_errorband

rng = np.random.default_rng(53176335)

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_low = y - 0.2
y_upp = y + 0.2

lp_config = LinePlotConfig(color="gold", linestyle="--", linewidth=2, marker="o", markersize=5, markeredgecolor="k")
ep_config = ErrorBandConfig(color="cyan", edgecolor="k", linestyle="--", hatch="\\")

ax = plot_errorband(
    x_data=x,
    y_data=y,
    y_lower=y_low,
    y_upper=y_upp,
    data_label=r"$\sin(X)$",
    band_config=ep_config,
    line_config=lp_config,
)

# plt.show()
plt.savefig("./images/README_example5.png", dpi=300)
plt.close()
