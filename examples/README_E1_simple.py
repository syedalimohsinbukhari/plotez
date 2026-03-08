"""Created on Mar 08 02:08:53 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

x = np.linspace(0, 10, 100)
y = np.sin(x)
plot_xy(x, y, auto_label=True)

# plt.show()
plt.savefig("./ex_images/README_E1_simple.png", dpi=300)
plt.close()
