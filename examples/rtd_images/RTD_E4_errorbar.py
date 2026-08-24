"""Created on Mar 08 02:43:18 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, plot_errorbar

rng = np.random.default_rng(1234)

x = np.linspace(0, 10, 20)
y = np.sin(x)
y_err = 0.3 * rng.random(size=y.shape)

plot_errorbar(x, y, y_err=y_err)

# plt.show()
plt.savefig("RTD_E4_errorbar.png", dpi=SAVE_DPI)
plt.close()
