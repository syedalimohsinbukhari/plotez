"""Created on Jul 20 00:17:08 2022."""

from .CONSTANTS import ERROR_ATTRS, LINE_ATTRS, SCATTER_ATTRS, SUBPLOT_ATTRS
from .error_handling import OrientationError
from .utilities import (
    ErrorPlot,
    LinePlot,
    ScatterPlot,
    SubPlots,
    dual_axes_data_validation,
    dual_axes_label_management,
    plot_or_scatter,
    split_dictionary,
)

__all__ = [
    "ERROR_ATTRS",
    "LINE_ATTRS",
    "SCATTER_ATTRS",
    "SUBPLOT_ATTRS",
    "OrientationError",
    "ErrorPlot",
    "LinePlot",
    "ScatterPlot",
    "SubPlots",
    "dual_axes_data_validation",
    "dual_axes_label_management",
    "plot_or_scatter",
    "split_dictionary",
]
