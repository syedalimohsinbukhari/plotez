"""Created on May 17 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import hgc, plot_hist

data = np.genfromtxt("../rtd_images/histogram_data.csv", delimiter=",", skip_header=1)
normal_data = data[:, 1]  # second column is 'normal'

h_cfg = hgc(bins=40, color="steelblue", ec="white", alpha=0.8)

plot_hist(
    normal_data,
    x_label="Value",
    y_label="Counts",
    plot_title="Histogram of Normal Distribution",
    data_label="Normal",
    hist_config=h_cfg,
)

# plt.show()
plt.savefig("README_E7_histogram.png", dpi=300)
plt.close()
