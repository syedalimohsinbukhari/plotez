"""Created on Mar 08 02:33:22 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import LinePlotConfig, plot_xyy

x = np.linspace(0, 10, 50)
y1, y2 = np.sin(x), np.cos(x)

# The `LinePlotConfig` class can also handle non-defined keywords using
# the `_extra` parameter
config = LinePlotConfig(
    linestyle=["--", "-."],
    color=["crimson", "gold"],
    marker=["o", "s"],
    markersize=[8, 8],
    markeredgecolor=["black", "black"],
    _extra={"markevery": [5, 5]},
)

plot_xyy(x, y1, y2, plot_config=config, auto_label=True)

# plt.show()
plt.savefig("./ex_images/README_E6_full_customization.png", dpi=300)
plt.close()
