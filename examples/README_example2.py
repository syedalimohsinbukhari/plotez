"""Created on Feb 16 11:26:26 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xyy

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(x / 10)

plot_xyy(
    x, y1, y2,
    x_label='Time',
    y1_label='Sine',
    y2_label='Exponential',
    data_labels=['sin(x)', 'exp(x/10)'],
    plot_title='Dual Y-Axis Example',
    use_twin_x=True
)

# plt.show()
plt.savefig("./images/README_example2.png")
plt.close()
