"""
PlotEZ - Mundane plotting made easy.

A Python library for simplified matplotlib plotting.
"""

from .plotez import (
    n_plotter,
    plot_errorbar,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xy,
    plot_xyy,
    two_subplots,
)
from .version import __version__

__all__ = [
    "plot_two_column_file",
    "plot_xy",
    "plot_xyy",
    "plot_with_dual_axes",
    "two_subplots",
    "n_plotter",
    "plot_errorbar",
    "__version__",
]
