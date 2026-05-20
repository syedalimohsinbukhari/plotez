"""Created on May 17 2026"""

import matplotlib.pyplot as plt
import numpy as np

from plotez import hgc, plot_density

data = np.genfromtxt("histogram_data.csv", delimiter=",", skip_header=1)
normal_data = data[:, 1]  # second column is 'normal'

h_cfg = hgc(bins=40, color="mediumpurple", ec="white", alpha=0.8)

ax = plot_density(
    x_data=normal_data,
    x_label="Value",
    y_label="Density",
    plot_title="Density Plot - Normal Distribution",
    data_label="Normal",
    hist_config=h_cfg,
)

plt.tight_layout()

# plt.show()
plt.savefig("RTD_E14_density.png", dpi=300)
plt.close()
