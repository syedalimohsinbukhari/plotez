"""Created on Mar 08 02:15:59 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import ErrorBandConfig, LinePlotConfig, plot_errorband

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_lower = y - 0.2
y_upper = y + 0.2

# Use ErrorBandConfig to customize the error band
band_config = ErrorBandConfig(color="darkblue", alpha=0.25)

# Use LinePlotConfig to customize the central line
plot_config = LinePlotConfig(color="gold", linewidth=2, linestyle="--", marker="o", markersize=5, markeredgecolor="k")

# Pass the configurations to the `plot_errorband` function
plot_errorband(x, y, y_lower, y_upper, data_label="Measurement", band_config=band_config, line_config=plot_config)

# plt.show()
plt.savefig("./ex_images/README_E5-1_error_band.png", dpi=300)
plt.close()
