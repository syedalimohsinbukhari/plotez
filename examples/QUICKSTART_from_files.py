"""Created on Feb 27 11:20:39 2026"""

import matplotlib.pyplot as plt

from plotez import plot_two_column_file

plot_two_column_file("data.csv")

plt.savefig("./images/QUICKSTART_from_files__no_style.png", dpi=300)

import matplotlib.pyplot as plt

from plotez import plot_two_column_file as ptcf

ptcf("data.csv", delimiter=",", skip_header=True, x_label="X Values", y_label="Y Values", plot_title="Data from CSV")

plt.savefig("./images/QUICKSTART_from_files__with_style.png", dpi=300)
plt.close()
