"""Created on Mar 08 02:40:12 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import SAVE_DPI, plot_xy

x = np.linspace(0, 10, 100)
y = np.sin(x)
plot_xy(x, y, data_label="X vs Y")

# plt.show()
plt.savefig("RTD_E1_simple.png", dpi=SAVE_DPI)
plt.close()
