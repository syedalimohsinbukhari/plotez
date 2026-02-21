"""Created on Feb 16 16:02:27 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_errorbar
from plotez.backend.utilities import ErrorPlot

# Generate sample data with errors
x = np.linspace(0, 10, 20)
x_err = 0.4
y = np.sin(x)
y_err = 0.1 * np.random.rand(len(y))

# Enhanced error bar styling
ep = ErrorPlot(error_color='red', error_line_width=2, capsize=8, cap_thickness=2, line_style=':', line_width=2,
               color='darkblue', marker='d', marker_size=6)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_dictionary=ep)
# plt.show()
plt.savefig('./images/README_example5.png', dpi=300)
plt.close()
