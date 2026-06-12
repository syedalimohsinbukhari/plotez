"""
PlotEZ Error Handling.

Custom exceptions for plotting operations.
"""


class PlotEZError(Exception):
    """Base class for exceptions related to plotting operations."""

    __module__ = "plotez"

    pass


class OrientationError(PlotEZError):
    """Is raised when an invalid or unexpected orientation is used in a plot."""

    __module__ = "plotez"

    pass


# ---------------------------------------------------------------------------
# Data errors
# ---------------------------------------------------------------------------


class DataError(PlotEZError):
    """Base class for data-related plotting errors."""

    __module__ = "plotez"

    pass


class ShapeError(DataError):
    """Is raised when an array has an unexpected or incompatible shape."""

    __module__ = "plotez"

    pass


class DataLengthError(DataError):
    """Is raised when an array has an unexpected or incompatible shape."""

    __module__ = "plotez"

    pass


class EmptyDataError(DataError):
    """Is raised when required primary x or y data is empty."""

    __module__ = "plotez"

    pass


class ColumnCountError(DataError):
    """Is raised when a data file does not contain exactly two columns."""

    pass


# ---------------------------------------------------------------------------
# Configuration errors
# ---------------------------------------------------------------------------


class ConfigurationError(PlotEZError):
    """Base class for plot configuration and parameter errors."""

    __module__ = "plotez"

    pass


class AxisLabelError(ConfigurationError):
    """Is raised when the `axis_labels` sequence does not contain exactly three elements."""

    __module__ = "plotez"

    pass


class TwinXDataError(ConfigurationError):
    """Is raised when `x2_data` is supplied for a dual-Y-axis (`use_twin_x=True`) plot."""

    __module__ = "plotez"

    pass


class TwinYDataError(ConfigurationError):
    """Is raised when `y2_data` is supplied for a dual-X-axis (`use_twin_x=False`) plot."""

    __module__ = "plotez"

    pass


class XArrayNot1D(ConfigurationError):
    """Is raised when the X dimension of a data array is not 1."""

    __module__ = "plotez"
    pass


class YArrayNot1D(ConfigurationError):
    """Is raised when the Y dimension of a data array is not 1."""

    __module__ = "plotez"
    pass
