"""Created on Jul 20 00:17:08 2022."""

from ._wrappers import (
    ebc,
    epc,
    error_band_configuration,
    error_plot_configuration,
    hgc,
    histogram_config,
    line_plot_configuration,
    lpc,
    scatter_plot_configuration,
    spc,
)
from .CONSTANTS import ERROR_ATTRS, ERROR_BAND_ATTRS, HIST_ATTRS, LINE_ATTRS, SCATTER_ATTRS
from .error_handling import (
    AxisLabelError,
    ColumnCountError,
    ConfigurationError,
    DataError,
    DataLengthError,
    EmptyDataError,
    OrientationError,
    PlotEZError,
    ShapeError,
    TwinXDataError,
    TwinYDataError,
)
from .utilities import (
    ErrorBandConfig,
    ErrorPlotConfig,
    HistogramConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    dual_axes_data_validation,
    plot_or_scatter,
    split_dictionary,
    validate_1d,
    validate_equal_length,
)

__all__ = [
    "ebc",
    "lpc",
    "epc",
    "spc",
    "hgc",
    "error_band_configuration",
    "line_plot_configuration",
    "error_plot_configuration",
    "scatter_plot_configuration",
    "histogram_config",
    "ERROR_ATTRS",
    "LINE_ATTRS",
    "SCATTER_ATTRS",
    "ERROR_BAND_ATTRS",
    "HIST_ATTRS",
    # Base errors
    "PlotEZError",
    "DataError",
    "ConfigurationError",
    # Data errors
    "ShapeError",
    "DataLengthError",
    "EmptyDataError",
    "ColumnCountError",
    # Configuration errors
    "OrientationError",
    "AxisLabelError",
    "TwinXDataError",
    "TwinYDataError",
    # Config classes
    "ErrorPlotConfig",
    "ErrorBandConfig",
    "LinePlotConfig",
    "ScatterPlotConfig",
    "HistogramConfig",
    # Utilities
    "dual_axes_data_validation",
    "plot_or_scatter",
    "split_dictionary",
    "validate_1d",
    "validate_equal_length",
]
