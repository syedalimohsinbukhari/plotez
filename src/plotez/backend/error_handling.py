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
    Specific exceptions related to plot configuration or data issues
    should inherit from this class.
    """

    pass


class OrientationError(PlotError):
    """
    Raised when an invalid or unexpected orientation is used in a plot.

    Notes
    -----
    This error occurs when the orientation parameter for a plot is set
    incorrectly or does not match the expected format.
    """

    pass
