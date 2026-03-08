"""Created on Mar 08 02:10:19 2026"""

import numpy as np
from matplotlib import pyplot as plt

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

rng = np.random.default_rng(1234)

x = np.linspace(0, 10, 20)
y = np.sin(x)
y_err = 0.2 * rng.random(size=y.shape)

ep = ErrorPlotConfig(color="darkblue", marker="o", capsize=5, ecolor="red", markerfacecolor="lime")
plot_errorbar(x, y, y_err=y_err, errorbar_config=ep, auto_label=True)

# plt.show()
plt.savefig("./ex_images/README_E2_scientific_errorbars.png", dpi=300)
plt.close()
