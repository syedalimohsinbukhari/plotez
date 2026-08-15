"""Created on Mar 08 02:56:28 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, LinePlotConfig, n_plotter

rng = np.random.default_rng(1234)

x_data = [np.linspace(0, 10, 100) for _ in range(4)]
y_data = [x * np.cos(x) for x in x_data]

fig_kwargs = {"sharex": True, "sharey": True, "figsize": (10, 8)}
line_plot_cfg = LinePlotConfig(
    color=["red", "blue", "green", "gold"],
    markeredgecolor=["k"] * 4,
    marker=["o", "s", "d", "^"],
    _extra={"markevery": [5, 2, 3, 10]},
)

n_plotter(
    x_data=x_data,
    y_data=y_data,
    n_rows=2,
    n_cols=2,
    plot_config=line_plot_cfg,
    figure_kwargs=fig_kwargs,
    data_labels=["X$_1$ vs Y$_1$", "X$_2$ vs Y$_2$", "X$_3$ vs Y$_3$", "X$_4$ vs Y$_4$"],
)

# plt.show()
plt.savefig("RTD_E10_shared_axes.png", dpi=SAVE_DPI)
plt.close()
