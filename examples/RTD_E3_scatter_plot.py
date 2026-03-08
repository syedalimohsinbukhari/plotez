"""Created on Mar 08 02:42:03 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xy

x = np.random.randn(100)
y = 2 * x + 1 + np.random.randn(100) * 0.5

# use of `is_scatter` parameter to generate the scatter plot
plot_xy(x, y, is_scatter=True, x_label="Feature X", y_label="Target Y", plot_title="Noisy Linear Relationship")

# plt.show()
plt.savefig("./rtd_images/RTD_E3_scatter_plot.png", dpi=300)
plt.close()
