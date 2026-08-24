"""Created on Aug 09, 2026"""

import matplotlib.pyplot as plt
import numpy as np

import plotez
from plotez import SAVE_DPI, hgc, plot_hist

data = np.genfromtxt("histogram_data.csv", delimiter=",", skip_header=1)
normal_data = data[:, 1]  # second column is 'normal'
h_cfg = hgc(bins=40, color="steelblue", ec="white", alpha=0.8)

fig = plt.figure(figsize=(15, 4.5))

# plotez does not auto-apply its style on import by default. Set PLOTEZ_AUTO_STYLE=1
# (or "true"/"yes") before `import plotez` to opt in globally instead of the runtime
# calls demonstrated below.
# Each axes below is created right after its style call -- matplotlib snapshots
# rcParams like `axes.grid`/`font.family` onto an Axes at creation time, so creating
# every panel upfront would make them all look identical regardless of later style calls.
ax1 = fig.add_subplot(1, 3, 1)
plot_hist(
    normal_data,
    x_label="Value",
    y_label="Counts",
    plot_title="Default (no plotez style)",
    data_label="Normal",
    hist_config=h_cfg,
    axis=ax1,
)

plotez.enable_style()
ax2 = fig.add_subplot(1, 3, 2)
plot_hist(
    normal_data,
    x_label="Value",
    y_label="Counts",
    plot_title="After enable_style()",
    data_label="Normal",
    hist_config=h_cfg,
    axis=ax2,
)

plotez.enable_style(grid=False)
ax3 = fig.add_subplot(1, 3, 3)
plot_hist(
    normal_data,
    x_label="Value",
    y_label="Counts",
    plot_title="enable_style(grid=False)",
    data_label="Normal",
    hist_config=h_cfg,
    axis=ax3,
)

for ax in (ax1, ax2, ax3):
    ax.legend(loc="best")

# plt.show()
plt.savefig("RTD_E16_style_comparison.png", dpi=SAVE_DPI)
plt.close()
