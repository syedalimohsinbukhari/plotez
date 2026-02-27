"""Created on Feb 27 10:58:03 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend import ErrorPlotConfig

rng = np.random.default_rng(35182962)

# Generate sample data with errors
x = np.linspace(0, 10, 20)
y = np.sin(x)
x_err = 0.25 * rng.random(len(x))
y_err = 0.3 * rng.random(len(y))

# Simple error bar plot
plot_errorbar(x, y, x_err=x_err, y_err=y_err)

# With custom styling
ep_config = ErrorPlotConfig(linestyle="--", capsize=5, color="blue")
plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep_config)

# plt.show()
plt.savefig("./images/QUICKSTART_basic_errorbar.png", dpi=300)
plt.close()
