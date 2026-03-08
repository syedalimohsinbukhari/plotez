"""Created on Mar 08 02:54:14 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import n_plotter
from plotez.backend import LinePlotConfig

x_data = [np.linspace(0, 10, 100) for _ in range(4)]
y_data = [np.sin(x_data[0]), np.cos(x_data[1]), np.tan(x_data[2] / 5), x_data[3] ** 2 / 50]

config = LinePlotConfig(color=["red", "blue", "green", "purple"])

n_plotter(
    x_data=x_data,
    y_data=y_data,
    n_rows=2,
    n_cols=2,
    data_labels=[r"$\sin(x)$", r"$\cos(x)$", r"$\tan(x/5)$", r"$x^2$/50"],
    plot_config=config,
)

# plt.show()
plt.savefig("./rtd_images/RTD_E9_grid_of_four.png", dpi=300)
plt.close()
