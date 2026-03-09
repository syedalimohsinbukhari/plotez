"""Created on Mar 08 02:15:59 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import ebc, lpc, plot_errorband

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_lower = y - 0.2
y_upper = y + 0.2

# `ebc` as a proxy to `ErrorBandConfig`: it uses conventional matplotlib parameter names
band_config = ebc(c="darkblue", alpha=0.25)

# `lpc` as a proxy to `LinePlotConfig`: it uses conventional matplotlib parameter names
plot_config = lpc(c="gold", lw=2, ls="--", marker="o", ms=5, mec="k")

# Pass the configurations to the `plot_errorband` function
plot_errorband(x, y, y_lower, y_upper, data_label="Measurement", band_config=band_config, line_config=plot_config)

# plt.show()
plt.savefig("./ex_images/README_E5-2_error_band.png", dpi=300)
plt.close()
