"""Created on Feb 16 16:02:27 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbars
from plotez.backend.utilities import ErrorPlot

# Generate sample data with errors
x = np.linspace(0, 10, 20)
x_err = 0.4
y = np.sin(x)
y_err = 0.1 * np.random.rand(len(y))

# Enhanced error bar styling
ep = ErrorPlot(
    line_style=':',
    line_width=2,
    color='darkblue',
    marker='d',
    marker_size=6,
    capsize=8,
    elinewidth=2,  # Error bar line width
    ecolor='red',  # Error bar color (different from line!)
    capthick=2  # Error bar cap thickness
)
plot_errorbars(x, y, x_err=x_err, y_err=y_err, plot_dictionary=ep)
# plt.show()
plt.savefig('./images/README_example5.png', dpi=300)
plt.close()
