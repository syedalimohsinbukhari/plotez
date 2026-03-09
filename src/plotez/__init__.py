"""
PlotEZ - Mundane plotting made easy.

A Python library for simplified matplotlib plotting.
"""

from .backend import (
    ErrorBandConfig,
    ErrorPlotConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    ebc,
    epc,
    error_band_configuration,
    error_plot_configuration,
    line_plot_configuration,
    lpc,
    scatter_plot_configuration,
    spc,
)
from .plotez import (
    n_plotter,
    plot_errorband,
    plot_errorbar,
    plot_two_column_file,
    plot_with_dual_axes,
    plot_xxy,
    plot_xy,
    plot_xyy,
    two_subplots,
)
from .version import __version__

__all__ = [
    # Plotting functions
    "plot_two_column_file",
    "plot_xy",
    "plot_xyy",
    "plot_xxy",
    "plot_with_dual_axes",
    "two_subplots",
    "n_plotter",
    "plot_errorbar",
    "plot_errorband",
    # Config classes
    "ErrorBandConfig",
    "ErrorPlotConfig",
    "LinePlotConfig",
    "ScatterPlotConfig",
    # Convenience / wrapper functions (long-form)
    "line_plot_configuration",
    "error_plot_configuration",
    "error_band_configuration",
    "scatter_plot_configuration",
    # Convenience / wrapper functions (short aliases)
    "lpc",
    "epc",
    "ebc",
    "spc",
    # Version
    "__version__",
]
