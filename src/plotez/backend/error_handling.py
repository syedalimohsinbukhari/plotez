"""
Ported from mpyez on Feb 15 09:28:37 2026

Created on Oct 21 00:12:02 2024
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


class NoXYLabels(PlotError):
    """
    Raised when x or y labels are missing in a plot.

    Notes
    -----
    This error occurs when a plot is expected to have labels for both
    the x-axis and y-axis, but one or both are missing. Proper labeling
    is often required for clarity in visualizations.
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
