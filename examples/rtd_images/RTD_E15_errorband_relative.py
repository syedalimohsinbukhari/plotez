"""Created on May 17, 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, ebc, lpc, plot_errorband_relative

x = np.linspace(0, 10, 200)
y = np.cos(x) + x * 0.25
y_err_lower = 0.15
y_err_upper = 0.25

band_cfg = ebc(c="lightcoral", alpha=0.35)
line_cfg = lpc(c="darkred", lw=2, markevery=10, marker="o")

ax = plot_errorband_relative(
    x_data=x,
    y_data=y,
    y_lower=y_err_lower,
    y_upper=y_err_upper,
    x_label="X",
    y_label="Y",
    plot_title="Relative Error Band",
    data_label=r"$[\cos(x) + x + 0.25]^{+0.25}_{-0.15}$",
    band_config=band_cfg,
    line_config=line_cfg,
)

# plt.show()
plt.savefig("RTD_E15_errorband_relative.png", dpi=SAVE_DPI)
plt.close()
