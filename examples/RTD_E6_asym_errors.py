"""Created on Mar 08 02:45:37 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar

x = np.linspace(0, 10, 20)
y = x**2 / 10

# Shape (2, N): [lower_errors, upper_errors]
y_err = np.array([0.1 * y, 0.35 * y])  # Lower (10% of value)  # Upper  (35% of value)
plot_errorbar(x, y, y_err=y_err, auto_label=True)

# plt.show()
plt.savefig("./rtd_images/RTD_E6_asym_errors.png", dpi=300)
plt.close()
