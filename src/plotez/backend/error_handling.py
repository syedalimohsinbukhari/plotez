"""
PlotEZ Error Handling.

Custom exceptions for plotting operations.
"""


class PlotError(Exception):
    """
    Base class for exceptions related to plotting operations.

    Notes
    -----
    This serves as the parent class for all plotting-related errors.
    Specific exceptions related to plot configuration or data issues should inherit from this class.
    """

    pass


class OrientationError(PlotError):
    """
    Raised when an invalid or unexpected orientation is used in a plot.

    Notes
    -----
    This error occurs when the orientation parameter for a plot is set incorrectly or does not match the expected
    format.
    """

    pass


# ---------------------------------------------------------------------------
# Data errors
# ---------------------------------------------------------------------------


class DataError(PlotError):
    """
    Base class for data-related plotting errors.

    Notes
    -----
    Inherit from this class for any error that stems from invalid, malformed, or incompatible input data arrays or
    files.
    """

    pass


class ShapeError(DataError):
    """
    Raised when an array has an unexpected or incompatible shape.

    Notes
    -----
    Typically raised when an error array intended for asymmetric error bars does not satisfy the required ``(2, N)``
    shape contract.
    """

    pass


class EmptyDataError(DataError):
    """
    Raised when required primary x or y data is empty.

    Notes
    -----
    At least one data point must be present in the primary x and y arrays before a plot can be constructed.
    """

    pass


class ColumnCountError(DataError):
    """
    Raised when a data file does not contain exactly two columns.

    Notes
    -----
    ``plot_two_column_file`` expects files with exactly one x-column and one y-column.
    Any other column count triggers this error.
    """

    pass


# ---------------------------------------------------------------------------
# Configuration errors
# ---------------------------------------------------------------------------


class ConfigurationError(PlotError):
    """
    Base class for plot configuration and parameter errors.

    Notes
    -----
    Inherit from this class for errors that arise from incorrect or conflicting plot configuration options rather than
    from the data itself.
    """

    pass


class AxisLabelError(ConfigurationError):
    """
    Raised when the ``axis_labels`` sequence does not contain exactly three elements.

    Notes
    -----
    Dual-axes functions require labels for three axes: primary x, primary y, and the secondary axis (either x or y).
    """

    pass


class TwinXDataError(ConfigurationError):
    """
    Is raised when ``x2_data`` is supplied for a dual-Y-axis (``use_twin_x=True``) plot.

    Notes
    -----
    A dual-Y-axis plot shares the x-axis between both datasets; providing a separate ``x2_data`` is therefore
    contradictory and not permitted.
    """

    pass


class TwinYDataError(ConfigurationError):
    """
    Is raised when ``y2_data`` is supplied for a dual-X-axis (``use_twin_x=False``) plot.

    Notes
    -----
    A dual-X-axis plot shares the y-axis between both datasets; providing a separate ``y2_data`` is therefore
    contradictory and not permitted.
    """

    pass


# ---------------------------------------------------------------------------
# Warnings
# ---------------------------------------------------------------------------


class LabelConflictWarning(UserWarning):
    """
    Issued when ``auto_label=True`` overrides user-provided labels.

    Notes
    -----
    When ``auto_label`` is enabled, it silently replaces any explicitly supplied axis labels, data labels,
    or plot titles with auto-generated defaults.
    This warning is raised to make that substitution visible to the caller.
    Use ``warnings.filterwarnings`` to suppress or escalate it as needed.
    """

    pass
