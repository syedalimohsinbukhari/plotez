"""Created on Feb 26 09:52:15 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez.backend import ErrorBandConfig, LinePlotConfig
from plotez.plotez import plot_errorband

rng = np.random.default_rng(1234)

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_low = y - 0.2
y_upp = y + 0.2

error_config = ErrorBandConfig(color="cyan", edgecolor="k", linestyle="--", hatch="\\")
line_config = LinePlotConfig(color="gold", linestyle="--", linewidth=2, marker="o", markersize=5, markeredgecolor="k")

ax = plot_errorband(x, y, y_low, y_upp, data_label=r"$\sin(X)$", band_config=error_config, line_config=line_config)
ax.legend()

# plt.show()
plt.savefig("./images/README_example5.png", dpi=300)
plt.close()
