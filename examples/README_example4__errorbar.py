"""Created on Feb 16 16:02:27 2026"""

import numpy as np
import matplotlib.pyplot as plt

from plotez.backend.utilities import ErrorPlot
from plotez.plotez import plot_errorbars

# Generate sample data
x = np.linspace(0, 10, 20)
y = np.sin(x)
x_err = 0.1 + 0.05 * np.random.rand(len(x))
y_err = 0.1 + 0.05 * np.random.rand(len(y))

# Example 1: Basic ErrorPlot (backward compatible)
print("Example 1: Basic ErrorPlot")
plt.figure(figsize=(16, 4))

plt.subplot(1, 3, 1)
ep1 = ErrorPlot(line_style='--', capsize=5, color='blue')
plot_errorbars(x, y, x_err, y_err, plot_dictionary=ep1)
plt.title("Basic ErrorPlot")
plt.xlabel("X")
plt.ylabel("Y")

# Example 2: Enhanced ErrorPlot with new error bar styling
print("Example 2: Enhanced ErrorPlot with error bar styling")
plt.subplot(1, 3, 2)
ep2 = ErrorPlot(
    line_style='-',
    line_width=2,
    color='darkblue',
    marker='o',
    marker_size=5,
    capsize=8,
    elinewidth=2,  # Error bar line width
    ecolor='red',  # Error bar color (different from line color!)
    capthick=2,  # Error bar cap thickness
    alpha=0.7
)
plot_errorbars(x, y, x_err, y_err, plot_dictionary=ep2)
plt.title("Enhanced with Error Bar Styling")
plt.xlabel("X")
plt.ylabel("Y")

# Example 3: Full LinePlot parameter support
print("Example 3: Full LinePlot parameter support")
plt.subplot(1, 3, 3)
ep3 = ErrorPlot(
    line_style='-.',
    line_width=1.5,
    color='green',
    marker='D',
    marker_size=6,
    marker_edge_color='black',
    marker_face_color='yellow',
    marker_edge_width=1.5,
    capsize=6,
    elinewidth=1.5,
    ecolor='orange',
    alpha=0.8
)
plot_errorbars(x, y, x_err, y_err, plot_dictionary=ep3)
plt.title("Full Customization")
plt.xlabel("X")
plt.ylabel("Y")

plt.tight_layout()
plt.savefig("images/errorplot_examples.png")
