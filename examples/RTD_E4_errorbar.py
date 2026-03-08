"""Created on Mar 08 02:43:18 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar

rng = np.random.default_rng(1234)

x = np.linspace(0, 10, 20)
y = np.sin(x)
y_err = 0.3 * rng.random(size=y.shape)

plot_errorbar(x, y, y_err=y_err, auto_label=True)

# plt.show()
plt.savefig("./rtd_images/RTD_E4_errorbar.png", dpi=300)
plt.close()
