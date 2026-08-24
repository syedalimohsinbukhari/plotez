"""Created on Mar 08 03:04:33 2026"""

import matplotlib.pyplot as plt

from plotez import SAVE_DPI, plot_two_column_file

plot_two_column_file(
    "sensor_data.csv",
    delimiter=",",
    skip_header=True,
    x_label="Time (s)",
    y_label="Temperature (°C)",
    data_label="Thermocouple",
    plot_title="Sensor Readings",
    is_scatter=True,
)

# plt.show()
plt.savefig("RTD_E11_from_files.png", dpi=SAVE_DPI)
plt.close()
