"""Created on Aug 09, 2026"""

import matplotlib.pyplot as plt
import numpy as np

import plotez
from plotez import plot_errorbar

rng = np.random.default_rng(7)
x = np.linspace(0, 10, 20)
y = np.sin(x)
y_err = 0.2 * rng.random(size=y.shape)

fig = plt.figure(figsize=(15, 4.5))

# plotez does not auto-apply its style on import by default. Set PLOTEZ_AUTO_STYLE=1
# (or "true"/"yes") before `import plotez` to opt in globally instead of calling
# enable_style() at runtime, as shown below.
# Each axes below is created right after its style call -- matplotlib snapshots
# rcParams like `axes.grid`/`font.family` onto an Axes at creation time, so creating
# every panel upfront would make them all look identical regardless of later style calls.
ax1 = fig.add_subplot(1, 3, 1)
plot_errorbar(x, y, y_err=y_err, plot_title="Default (no plotez style)", data_label="sin(x)", axis=ax1)

plotez.enable_style()
ax2 = fig.add_subplot(1, 3, 2)
plot_errorbar(x, y, y_err=y_err, plot_title="After enable_style()", data_label="sin(x)", axis=ax2)

plotez.disable_style()
ax3 = fig.add_subplot(1, 3, 3)
plot_errorbar(x, y, y_err=y_err, plot_title="After disable_style()", data_label="sin(x)", axis=ax3)

for ax in (ax1, ax2, ax3):
    ax.legend(loc="best")

plt.tight_layout()

# plt.show()
plt.savefig("README_E8_style_comparison.png", dpi=300)
plt.close()
