"""Created on Mar 08 02:40:12 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

x = np.linspace(0, 10, 100)
y = np.sin(x)
plot_xy(x, y, auto_label=True)

# plt.show()
plt.savefig("./rtd_images/RTD_E1_simple.png", dpi=300)
plt.close()
