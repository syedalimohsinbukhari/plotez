"""Created on Feb 16 11:27:55 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import n_plotter

# Create 2×2 grid
x_data = [np.linspace(0, 10, 100) for _ in range(4)]
y_data = [
    np.sin(x_data[0]),
    np.cos(x_data[1]),
    np.tan(x_data[2] / 5),
    x_data[3]**2 / 100
]

fig, axs = n_plotter(
    x_data, y_data,
    n_rows=2, n_cols=2,
    auto_label=True
)

# plt.show()
plt.savefig("./images/README_example3.png")
plt.close()
