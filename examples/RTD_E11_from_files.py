"""Created on Mar 08 03:04:33 2026"""

import matplotlib.pyplot as plt

from plotez import plot_two_column_file

plot_two_column_file(
    "sensor_data.csv",
    delimiter=",",
    skip_header=True,
    x_label="Time (s)",
    y_label="Temperature (°C)",
    plot_title="Sensor Readings",
    data_label="Thermocouple",
    is_scatter=True,
)

# plt.show()
plt.savefig("./rtd_images/RTD_E11_from_files.png", dpi=300)
plt.close()
