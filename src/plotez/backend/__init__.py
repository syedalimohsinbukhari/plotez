"""Created on Jul 20 00:17:08 2022."""

from ._wrappers import (
    ebc,
    epc,
    error_band_configuration,
    error_plot_configuration,
    line_plot_configuration,
    lpc,
    scatter_plot_configuration,
    spc,
)
from .CONSTANTS import ERROR_ATTRS, ERROR_BAND_ATTRS, LINE_ATTRS, SCATTER_ATTRS
from .error_handling import (
    AxisLabelError,
    ColumnCountError,
    ConfigurationError,
    DataError,
    EmptyDataError,
    LabelConflictWarning,
    OrientationError,
    PlotError,
    ShapeError,
    TwinXDataError,
    TwinYDataError,
)
from .utilities import (
    ErrorBandConfig,
    ErrorPlotConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    dual_axes_data_validation,
    dual_axes_label_management,
    plot_or_scatter,
    split_dictionary,
)

__all__ = [
    "ebc",
    "lpc",
    "epc",
    "spc",
    "error_band_configuration",
    "line_plot_configuration",
    "error_plot_configuration",
    "scatter_plot_configuration",
    "ERROR_ATTRS",
    "LINE_ATTRS",
    "SCATTER_ATTRS",
    "ERROR_BAND_ATTRS",
    # Base errors
    "PlotError",
    "DataError",
    "ConfigurationError",
    # Data errors
    "ShapeError",
    "EmptyDataError",
    "ColumnCountError",
    # Configuration errors
    "OrientationError",
    "AxisLabelError",
    "TwinXDataError",
    "TwinYDataError",
    # Warnings
    "LabelConflictWarning",
    # Config classes
    "ErrorPlotConfig",
    "ErrorBandConfig",
    "LinePlotConfig",
    "ScatterPlotConfig",
    # Utilities
    "dual_axes_data_validation",
    "dual_axes_label_management",
    "plot_or_scatter",
    "split_dictionary",
]
