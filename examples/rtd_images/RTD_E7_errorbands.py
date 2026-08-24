"""Created on Mar 08 02:46:45 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, ErrorBandConfig, LinePlotConfig, plot_errorband

x = np.linspace(0, 10, 200)  # Dense sampling
y = np.sin(x)
y_lower = y - 0.15
y_upper = y + 0.15

band_cfg = ErrorBandConfig(color="lightblue", alpha=0.4)
line_cfg = LinePlotConfig(color="navy", linewidth=2, marker="s", _extra={"markevery": 5})

plot_errorband(
    x_data=x,
    y_data=y,
    y_lower=y_lower,
    y_upper=y_upper,
    data_label=r"$\sin(x) \pm 0.15$",
    band_config=band_cfg,
    line_config=line_cfg,
)

# plt.show()
plt.savefig("RTD_E7_errorbands.png", dpi=SAVE_DPI)
plt.close()
