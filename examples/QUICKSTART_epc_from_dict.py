"""Created on Feb 27 11:08:14 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

rng = np.random.default_rng(4352456245)

# Generate sample data with errors
x = np.linspace(0, 10, 20)
y = np.sin(x)
x_err = 0.25 * rng.random(len(x))
y_err = 0.3 * rng.random(len(y))

# Simple error bar plot
plot_errorbar(x, y, x_err=x_err, y_err=y_err)

# Using parameter aliases
params = {
    "ls": "--",  # linestyle
    "lw": 2,  # linewidth
    "color": "purple",
    "marker": "s",
    "ms": 6,  # markersize
    "capsize": 7,
    "elinewidth": 2,
    "ecolor": "crimson",
}

ep_config = ErrorPlotConfig.populate(params)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep_config)

# plt.show()
plt.savefig("./images/QUICKSTART_epc_from_dict.png", dpi=300)
plt.close()
