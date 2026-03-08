"""Created on Mar 08 02:51:07 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import FigureConfig, two_subplots

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

two_subplots(
    x_data=[x, x],
    y_data=[y1, y2],
    orientation="v",
    subplot_title=["Sine", "Cosine"],
    figure_config=FigureConfig(figsize=(6, 8)),
)

# plt.show()
plt.savefig("./rtd_images/RTD_E8_two_subplots.png", dpi=300)
plt.close()
