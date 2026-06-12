"""Custom exceptions raised by PlotEZ."""

__all__ = [
    "AxisLabelError",
    "ColumnCountError",
    "ConfigurationError",
    "DataError",
    "DataLengthError",
    "EmptyDataError",
    "OrientationError",
    "PlotEZError",
    "ShapeError",
    "TwinXDataError",
    "TwinYDataError",
    "XArrayNot1D",
    "YArrayNot1D",
]


class PlotEZError(Exception):
    """Base class for exceptions related to plotting operations."""


class OrientationError(PlotEZError):
    """Raised when an invalid or unexpected plot orientation is used."""


class DataError(PlotEZError):
    """Base class for data-related plotting errors."""


class ShapeError(DataError):
    """Raised when an array has an unexpected or incompatible shape."""


class DataLengthError(DataError):
    """Raised when arrays that must align have incompatible lengths."""


class EmptyDataError(DataError):
    """Raised when required primary x or y data is empty."""


class ColumnCountError(DataError):
    """Raised when a data file does not contain exactly two columns."""


class ConfigurationError(PlotEZError):
    """Base class for plot configuration and parameter errors."""


class AxisLabelError(ConfigurationError):
    """Raised when ``axis_labels`` does not contain exactly three elements."""


class TwinXDataError(ConfigurationError):
    """Raised when ``x2_data`` is supplied for a dual-Y-axis plot."""


class TwinYDataError(ConfigurationError):
    """Raised when ``y2_data`` is supplied for a dual-X-axis plot."""


class XArrayNot1D(ConfigurationError):
    """Raised when the x dimension of a data array is not one-dimensional."""


class YArrayNot1D(ConfigurationError):
    """Raised when the y dimension of a data array is not one-dimensional."""
