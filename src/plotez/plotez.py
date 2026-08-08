"""
PlotEZ - Mundane plotting made easy.

This module provides simplified plotting functions for common visualization tasks.
"""

from __future__ import annotations

__all__ = [
    "plot_errorband",
    "plot_errorband_relative",
    "plot_errorbar",
    "plot_two_column_file",
    "plot_xy",
    "plot_xyy",
    "plot_xxy",
    "plot_with_dual_axes",
    "two_subplots",
    "n_plotter",
    "plot_density",
    "plot_hist",
    "plot_bar",
    "plot_barh",
]

from typing import Any
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np

from .backend.base_config import PlotEZConfig
from .backend.utilities import (
    dual_axes_data_validation,
    error_band_validation,
    error_offset_validation,
    errorbar_validation,
    plot_or_scatter,
    validate_1d,
    validate_equal_length,
)
from .configurations import (
    BarPlotConfig,
    ErrorBandConfig,
    ErrorPlotConfig,
    HistogramConfig,
    LinePlotConfig,
    ScatterPlotConfig,
)
from .errors import ColumnCountError, ConfigurationError, DataError, EmptyDataError, OrientationError
from .typing import ArrayLike, Axes, AxesReturn, NDArray

# =============================================================================
# Helper functions
# =============================================================================


def _config_handler(
    input_config: PlotEZConfig | dict[str, Any] | None, default_config: type[PlotEZConfig]
) -> dict[str, Any]:
    if isinstance(input_config, dict):
        config = default_config.populate(input_config).get_dict()
    elif isinstance(input_config, default_config):
        config = input_config.get_dict()
    else:
        config = default_config().get_dict()

    return config


def _fig_kwargs_handler(axis, fig_kwargs) -> Axes:
    if axis is not None:
        if fig_kwargs:
            warn(message="`figure_kwargs` is ignored when `axis` is provided.", category=UserWarning, stacklevel=3)
    else:
        _, axis = plt.subplots(**(fig_kwargs or {}))

    return axis


def _label_sanitizer(
    n_rows: int,
    n_cols: int,
    x_labels: list[str] | tuple[str, ...] | None,
    y_labels: list[str] | tuple[str, ...] | None,
    data_labels: list[str] | tuple[str, ...] | None,
    subplot_titles: list[str] | tuple[str, ...] | None,
    plot_title: str | None,
) -> tuple[list[str], list[str], list[str], list[str], str]:
    n = n_rows * n_cols

    def _pad(labels: list[str] | tuple[str, ...] | None, name: str) -> list[str]:
        if labels is None:
            return [""] * n
        normalized = list(labels)
        if len(normalized) < n:
            warn(
                message=f"`{name}` has {len(normalized)} element(s) but a {n_rows}×{n_cols} grid ({n} subplots) was "
                f"requested. Padding with empty strings for the remaining {n - len(normalized)}.",
                category=UserWarning,
                stacklevel=3,
            )
            return normalized + [""] * (n - len(normalized))
        if len(normalized) > n:
            warn(
                message=f"`{name}` has {len(normalized)} element(s) but a {n_rows}x{n_cols} grid "
                f"({n} subplots) was requested. Trimming the last {len(normalized) - n} element(s).",
                category=UserWarning,
                stacklevel=3,
            )
            return normalized[:n]
        return normalized

    return (
        _pad(labels=x_labels, name="x_labels"),
        _pad(labels=y_labels, name="y_labels"),
        _pad(labels=data_labels, name="data_labels"),
        _pad(labels=subplot_titles, name="subplot_titles"),
        plot_title or "",
    )


# =============================================================================
# Error Visualization Functions
# =============================================================================


def plot_errorband_relative(
    x_data: ArrayLike,
    y_data: ArrayLike,
    y_lower: float | ArrayLike | None = None,
    y_upper: float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBand",
    data_label: str = "X vs. Y",
    line: bool = True,
    band_config: ErrorBandConfig | None = None,
    line_config: LinePlotConfig | dict[str, Any] | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> Axes:
    """
    Plot a line graph with a shaded error band using relative (offset) errors.

    A convenience wrapper around :func:`plot_errorband` where `y_lower` and `y_upper` are interpreted as offsets
    from `y_data` rather than absolute bounds.
    Internally, the absolute bounds are computed as `y_data - y_lower` and `y_data + y_upper` before passing
    to :func:`plot_errorband`.

    Parameters
    ----------
    x_data :
        The independent variable values to plot.
    y_data :
        The central values to plot.
    y_lower :
        The downward offset from `y_data` defining the lower band edge.
        If `None`, it is inferred as equal to `y_upper`, implying a symmetric band.
        At least one of `y_lower` or `y_upper` must be provided.
    y_upper :
        The upward offset from `y_data` defining the upper band edge.
        If `None`, it is inferred as equal to `y_lower`, implying a symmetric band.
        At least one of `y_lower` or `y_upper` must be provided.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title of the plot.
    data_label :
        The label for the data series, used in the legend.
        If `line=True`, the label is attached to the line.
        If `line=False`, it is attached to the band.
    line :
        Whether to draw a line through the central values over the error band.
    band_config :
        Configuration for the error band styling.
        If `None`, defaults are used.
    line_config :
        Configuration for the line styling.
        If `None`, defaults are used.
    axis :
        Pre-existing Matplotlib axes to draw on.
        If provided, `figure_kwargs` is ignored.
    figure_kwargs :
        Keyword arguments passed to `plt.subplots` when creating a new figure.
        Ignored if `axis` is provided.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.

    Raises
    ------
    ConfigurationError
        If both `y_lower` and `y_upper` are `None`.
    ShapeError
        If data or an array-valued offset is not one-dimensional.
    DataLengthError
        If an array-valued offset does not match ``y_data``.

    See Also
    --------
    plot_errorband : The absolute-bounds version of this function.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    validate_1d(x, y, names=["x_data", "y_data"])

    lower_offset, upper_offset = error_offset_validation(y=y, y_lower=y_lower, y_upper=y_upper)

    return plot_errorband(
        x_data=x,
        y_data=y,
        y_lower=(y - lower_offset) if lower_offset is not None else None,
        y_upper=(y + upper_offset) if upper_offset is not None else None,
        x_label=x_label,
        y_label=y_label,
        plot_title=plot_title,
        data_label=data_label,
        line=line,
        band_config=band_config,
        line_config=line_config,
        axis=axis,
        figure_kwargs=figure_kwargs,
    )


def plot_errorband(
    x_data: ArrayLike,
    y_data: ArrayLike,
    y_lower: float | ArrayLike | None = None,
    y_upper: float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBand",
    data_label: str = "X vs. Y",
    line: bool = True,
    band_config: ErrorBandConfig | dict[str, Any] | None = None,
    line_config: LinePlotConfig | dict[str, Any] | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> Axes:
    """
    Plot a line graph with a shaded error band representing uncertainty.

    Parameters
    ----------
    x_data :
        The independent variable values to plot.
    y_data :
        The central values to plot.
    y_lower :
        The lower bound of the error band.
        If `None`, it is inferred as a symmetric reflection of `y_upper` through `y_data`.
        At least one of `y_lower` or `y_upper` must be provided.
    y_upper :
        The upper bound of the error band.
        If `None`, it is inferred as a symmetric reflection of `y_lower` through `y_data`.
        At least one of `y_lower` or `y_upper` must be provided.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title of the plot.
    data_label :
        The label for the data series, used in the legend.
        If `line=True`, the label is attached to the line.
        If `line=False`, it is attached to the band.
    line :
        Whether to draw a line through the central values over the error band.
    band_config :
        Configuration for the error band styling.
        If `None`, defaults are used.
    line_config :
        Configuration for the line styling.
        If `None`, defaults are used.
    axis :
        Pre-existing Matplotlib axes to draw on.
        If provided, `figure_kwargs` is ignored.
    figure_kwargs :
        Keyword arguments passed to `plt.subplots` when creating a new figure.
        Ignored if `axis` is provided.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.

    Raises
    ------
    ConfigurationError
        If both `y_lower` and `y_upper` are `None`.
    ShapeError
        If data or an array-valued bound is not one-dimensional.
    DataLengthError
        If data and array-valued bounds do not have matching lengths.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    validate_1d(x, y, names=["x_data", "y_data"])
    validate_equal_length(x, y, names=["x_data", "y_data"])

    y_lower, y_upper = error_band_validation(x=x, y=y, y_lower=y_lower, y_upper=y_upper)

    if y_lower is None:
        y_lower = y - (y_upper - y)
    elif y_upper is None:
        y_upper = y + (y - y_lower)

    if axis is not None:
        axis = axis
        if figure_kwargs:
            warn(message="`figure_kwargs` is ignored when `axis` is provided.", category=UserWarning, stacklevel=2)
    else:
        _, axis = plt.subplots(**(figure_kwargs or {}))

    ebc = _config_handler(input_config=band_config, default_config=ErrorBandConfig)
    if isinstance(line_config, dict):
        line_config: LinePlotConfig = LinePlotConfig.populate(line_config)
    l_conf = _config_handler(input_config=line_config, default_config=LinePlotConfig)

    if line:
        _data_label = data_label or l_conf.get("label") or None

        if data_label and "label" in l_conf:
            warn("Both `data_label` and `line_config['label']` are provided. Using `data_label`.")

            l_conf.pop("label", None)

        axis.fill_between(x=x, y1=y_lower, y2=y_upper, **ebc)
        axis.plot(x, y, label=_data_label, **l_conf)
    else:
        axis.fill_between(x=x, y1=y_lower, y2=y_upper, label=data_label, **ebc)

    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_title(plot_title)
    axis.legend()

    return axis


def plot_errorbar(
    x_data: ArrayLike,
    y_data: ArrayLike,
    x_err: float | ArrayLike | None = None,
    y_err: float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBar",
    data_label: str = "X vs. Y",
    errorbar_config: ErrorPlotConfig | dict[str, Any] | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> Axes:
    """
    Plot an error bar graph with optional error ranges, labels, and configurations.

    Parameters
    ----------
    x_data :
        The x-coordinates of the data points.
    y_data :
        The y-coordinates of the data points.
    x_err :
        Error margins for x-coordinates. Can be:
        - Scalar: symmetric error for all points
        - 1D array (N,): symmetric errors, one per point
        - 2D array (2, N): asymmetric [lower_errors, upper_errors]
    y_err :
        Error margins for y-coordinates. Can be:
        - Scalar: symmetric error for all points
        - 1D array (N,): symmetric errors, one per point
        - 2D array (2, N): asymmetric [lower_errors, upper_errors]
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title of the plot.
    data_label :
        The label for the data points, which will appear in the plot legend.
        If `None`, the legend is not displayed.
    errorbar_config :
        Custom configurations for the error bars. If `None`, default configurations are used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        A matplotlib Axes object on which the plot will be rendered.
        If `None`, a new subplot is created using `figure_kwargs`.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.

    Raises
    ------
    ShapeError
        If x/y data is not one-dimensional or an asymmetric error array is not shaped ``(2, N)``.
    DataLengthError
        If x/y data or an error array has an incompatible length.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    validate_1d(x, y, names=["x_data", "y_data"])
    x_err, y_err = errorbar_validation(x=x, y=y, x_err=x_err, y_err=y_err)

    ebc = _config_handler(input_config=errorbar_config, default_config=ErrorPlotConfig)

    axis = _fig_kwargs_handler(axis=axis, fig_kwargs=figure_kwargs)
    axis.errorbar(x=x, y=y, xerr=x_err, yerr=y_err, label=data_label, **ebc)

    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_title(plot_title)
    axis.legend()

    return axis


# =============================================================================
# File I/O Functions
# =============================================================================


def plot_two_column_file(
    file_name: str,
    delimiter: str = ",",
    skip_header: bool = False,
    x_label: str = "X",
    y_label: str = "Y",
    data_label: str = "XY Data",
    plot_title: str = "XY Plot",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> Axes:
    """Read a two-column file (x, y) and plot the data.

    Parameters
    ----------
    file_name :
        The path to the file to be plotted. The file should contain two columns (x and y data).
    delimiter :
        The delimiter used in the file (default is ',').
    skip_header :
        If True, skips the first row in the given data file, otherwise does nothing. Default is False.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    data_label :
        Data label for the plot to put in the legend. Defaults to 'X vs Y'.
    plot_title :
        The title for the plot.
    is_scatter :
        If True, creates a scatter plot. Otherwise, creates a line plot. Default is False.
    plot_config :
        Configuration object for line or scatter styling. If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.

    Returns
    -------
    Axes
        The axes object of the plot.

    Raises
    ------
    EmptyDataError
        If the file is empty or contains only one data row.
    ColumnCountError
        If the file does not contain exactly two columns.
    """
    data = np.genfromtxt(fname=file_name, delimiter=delimiter, skip_header=skip_header)

    if data.ndim == 1 or data.shape[0] == 0:
        raise EmptyDataError("File contains no data rows.")
    if data.shape[1] != 2:
        raise ColumnCountError("The file must contain exactly two columns of data.")

    x_data, y_data = data.T

    return plot_xy(
        x_data=x_data,
        y_data=y_data,
        x_label=x_label,
        y_label=y_label,
        data_label=data_label,
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )


# =============================================================================
# Simple Plotting Functions
# =============================================================================


def plot_xy(
    x_data: ArrayLike,
    y_data: ArrayLike,
    x_label: str = "X",
    y_label: str = "Y",
    data_label: str = "XY Data",
    plot_title: str = "XY Plot",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> Axes:
    """Plot the x_data against y_data with customizable options.

    Parameters
    ----------
    x_data :
        The data for the x-axis.
    y_data :
        The data for the y-axis.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title for the plot.
    data_label :
        Data label for the plot to put in the legend.
    is_scatter :
        If True, creates a scatter plot. Otherwise, creates a line plot.
        Defaults is False.
    plot_config :
        Configuration object for line or scatter styling.
        If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided.
        Ignored if `axis` is provided.
    axis :
        The axis object to draw the plots on.
        If not passed, a new axis object will be created internally.

    Returns
    -------
    Axes :
        The axis object of the plot.

    Raises
    ------
    ShapeError
        If ``x_data`` or ``y_data`` is not one-dimensional.
    DataLengthError
        If ``x_data`` and ``y_data`` have different lengths.
    """
    x_data, y_data = np.asarray(x_data), np.asarray(y_data)

    validate_1d(x_data, y_data, names=["x_data", "y_data"])
    validate_equal_length(x_data, y_data, names=["x_data", "y_data"])

    axis = plot_with_dual_axes(
        x1_data=x_data,
        y1_data=y_data,
        x1y1_label=data_label,
        use_twin_x=False,
        axis_labels=(x_label, y_label, ""),
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )

    assert isinstance(axis, Axes), f"Expected `Axes` object, got `{type(axis)}`"
    return axis


# =============================================================================
# Dual-Axis Plotting Functions
# =============================================================================


def plot_xyy(
    x_data: ArrayLike,
    y1_data: ArrayLike,
    y2_data: ArrayLike,
    x_label: str = "X",
    y1_label: str = r"Y$_1$",
    y2_label: str = r"Y$_2$",
    data_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    plot_title: str = "XYY Plot",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> tuple[Axes, Axes]:
    """Plot two sets of y-data (`y1_data` and `y2_data`) against the same x-data (`x_data`) on the same plot.

    Parameters
    ----------
    x_data :
        The x-axis data for both plots.
    y1_data :
        The first set of y-axis data to be plotted against `x_data`.
    y2_data :
        The second set of y-axis data to be plotted against `x_data`.
    x_label :
        The label for the x-axis.
    y1_label :
        The label for the first y-axis.
    y2_label :
        The label for the second y-axis.
    plot_title :
        The title for the plot.
    data_labels :
        The labels for the two datasets. Default is `(r"X vs. Y$_1$", r"X vs. Y$_2$")`.
    is_scatter :
        Whether to create a scatter plot (`True`) or a line plot (`False`). Default is `False`.
    plot_config :
        Configuration object for line or scatter styling.
        If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided.
        Ignored if `axis` is provided.
    axis :
        A Matplotlib axis to plot on.
        If `None`, a new axis is created. Default is `None`.

    Returns
    -------
    tuple[Axes, Axes]
        A tuple of `(primary_axis, secondary_axis)` for the dual y-axis plot.

    Raises
    ------
    ShapeError
        If any data array is not one-dimensional.
    DataLengthError
        If ``x_data``, ``y1_data``, and ``y2_data`` have different lengths.
    """
    x_data, y1_data, y2_data = np.asarray(x_data), np.asarray(y1_data), np.asarray(y2_data)

    # both x_data, y1_data, and y2_data must be 1D arrays
    validate_1d(x_data, y1_data, y2_data, names=["x_data", "y1_data", "y2_data"])
    validate_equal_length(x_data, y1_data, y2_data, names=["x_data", "y1_data", "y2_data"])

    _data_labels: list[str] = list(data_labels) if data_labels is not None else [r"X vs. Y$_1$", r"X vs. Y$_2$"]

    axis = plot_with_dual_axes(
        x1_data=x_data,
        y1_data=y1_data,
        y2_data=y2_data,
        x1y1_label=_data_labels[0],
        x1y2_label=_data_labels[1],
        use_twin_x=True,
        axis_labels=(x_label, y1_label, y2_label),
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )

    axis: tuple[Axes, Axes]
    return axis


def plot_xxy(
    x1_data: ArrayLike,
    x2_data: ArrayLike,
    y_data: ArrayLike,
    y_label: str = "Y",
    x1_label: str = r"X$_1$",
    x2_label: str = r"X$_2$",
    data_labels: list[str] | tuple[str, ...] | None = None,
    plot_title: str = "",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> tuple[Axes, Axes]:
    """Plot two sets of x-data (`x1_data` and `x2_data`) against the same y-data (`y_data`) on the same plot.

    Parameters
    ----------
    x1_data :
        The first set of x-axis data to be plotted against `y_data`.
    x2_data :
        The second set of x-axis data to be plotted against `y_data`.
    y_data :
        The y-axis data for both plots.
    x1_label :
        The label for the first x-axis.
    x2_label :
        The label for the second x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title for the plot.
    data_labels :
        The labels for the two datasets.
        Default is `(r"Y vs. X$_1$", r"Y vs. X$_2$")`.
    is_scatter :
        Whether to create a scatter plot (`True`) or a line plot (`False`).
        Defaults is `False`.
    plot_config :
        Configuration object for line or scatter styling.
        If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided.
        Ignored if `axis` is provided.
    axis :
        A Matplotlib axis to plot on.
        If `None`, a new axis is created. Default is `None`.

    Returns
    -------
    tuple[Axes, Axes]
        A tuple of `(primary_axis, secondary_axis)` for the dual x-axis plot.

    Raises
    ------
    ShapeError
        If any data array is not one-dimensional.
    DataLengthError
        If ``x1_data``, ``x2_data``, and ``y_data`` have different lengths.
    """
    x1_data, x2_data, y_data = np.asarray(x1_data), np.asarray(x2_data), np.asarray(y_data)

    validate_1d(x1_data, x2_data, y_data, names=["x1_data", "x2_data", "y_data"])
    validate_equal_length(x1_data, x2_data, y_data, names=["x1_data", "x2_data", "y_data"])

    _data_labels: list[str] = list(data_labels) if data_labels is not None else [r"Y vs. X$_1$", r"Y vs. X$_2$"]

    axis = plot_with_dual_axes(
        x1_data=x1_data,
        y1_data=y_data,
        x2_data=x2_data,
        x1y1_label=_data_labels[0],
        x2y1_label=_data_labels[1],
        use_twin_x=False,
        axis_labels=(x1_label, y_label, x2_label),
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )

    axis: tuple[Axes, Axes]
    return axis


def plot_with_dual_axes(
    x1_data: ArrayLike,
    y1_data: ArrayLike,
    x2_data: ArrayLike | None = None,
    y2_data: ArrayLike | None = None,
    x1y1_label: str = r"X$_1$ vs. Y$_1$",
    x1y2_label: str = r"X$_1$ vs. Y$_2$",
    x2y1_label: str = r"X$_2$ vs. Y$_1$",
    use_twin_x: bool = False,
    axis_labels: list[str] | tuple[str, ...] | None = None,
    plot_title: str = "DualAxesPlot",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> AxesReturn:
    """Plot the data with options for dual axes (x or y) or single axis.

    Parameters
    ----------
    x1_data :
        Data for the primary x-axis.
    y1_data :
        Data for the primary y-axis.
    x2_data :
        Data for the secondary x-axis (used for dual x-axis plots).
    y2_data :
        Data for the secondary y-axis (used for dual y-axis plots).
    x1y1_label :
        Label for the plot of X1 vs. Y1.
    x1y2_label :
        Label for the plot of X1 vs. Y2 (when using dual Y-axes).
    x2y1_label :
        Label for the plot of X2 vs. Y1 (when using dual X-axes).
    use_twin_x :
        If True, creates a dual y-axis plot. If False, creates a dual x-axis plot.
        Default is False.
    axis_labels :
        List or tuple of axis labels in the form
        `[x_label, y_label1, y_label2]`.
        Defaults to `["X", r"Y$_1$", r"Y$_2$"]` when not provided.
    plot_title :
        Title of the plot.
    is_scatter :
        If True, creates scatter plot; otherwise, line plot. Default is False.
    plot_config :
        Configuration object for line or scatter styling. If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.

    Returns
    -------
    tuple[Axes, Axes] or Axes
        A tuple of `(primary_axis, secondary_axis)` when dual axes are used, otherwise a single `Axes`.
    """
    _axis_labels: list[str] = list(axis_labels) if axis_labels is not None else ["X", r"Y$_1$", r"Y$_2$"]

    x1_data, y1_data, x2_data, y2_data = dual_axes_data_validation(
        x1_data=x1_data,
        x2_data=x2_data,
        y1_data=y1_data,
        y2_data=y2_data,
        use_twin_x=use_twin_x,
        axis_labels=_axis_labels,
    )

    if axis is not None:
        ax1 = axis
    else:
        _, ax1 = plt.subplots(**(figure_kwargs or {}))

    if plot_config is not None:
        plot_dict = plot_config.get_dict()
    else:
        plot_dict = ScatterPlotConfig().get_dict() if is_scatter else LinePlotConfig().get_dict()

    dict1 = {key: (value[0] if isinstance(value, list) else value) for key, value in plot_dict.items()}
    plot_or_scatter(axis=ax1, scatter=is_scatter)(x1_data, y1_data, label=x1y1_label, **dict1)

    ax2 = None

    ax1.set_xlabel(_axis_labels[0])
    ax1.set_ylabel(_axis_labels[1])
    if plot_title:
        ax1.set_title(plot_title)

    dict2 = {
        key: (
            value[1] if isinstance(value, list) and len(value) > 1 else (value[0] if isinstance(value, list) else value)
        )
        for key, value in plot_dict.items()
    }

    if use_twin_x:
        ax2 = ax1.twinx()
        ax2.grid(False)  # avoid a second, misaligned grid from the twin axis's own scale
        if y2_data is not None:
            plot_or_scatter(axis=ax2, scatter=is_scatter)(x1_data, y2_data, label=x1y2_label, **dict2)
            ax2.set_ylabel(_axis_labels[2])

    elif x2_data is not None:
        ax2 = ax1.twiny()
        ax2.grid(False)  # avoid a second, misaligned grid from the twin axis's own scale
        plot_or_scatter(axis=ax2, scatter=is_scatter)(x2_data, y1_data, label=x2y1_label, **dict2)
        ax2.set_xlabel(_axis_labels[2])

    if x1y1_label or x1y2_label or x2y1_label:
        handles, labels = ax1.get_legend_handles_labels()
        if ax2:
            handles2, labels2 = ax2.get_legend_handles_labels()
            handles += handles2
            labels += labels2
        ax1.legend(handles, labels, loc="best")

    return ax1 if ax2 is None else (ax1, ax2)


# =============================================================================
# Multi-Panel Plotting Functions
# =============================================================================


def two_subplots(
    x_data: ArrayLike | list[ArrayLike],
    y_data: ArrayLike | list[ArrayLike],
    x_labels: list[str] | tuple[str, ...] | None = None,
    y_labels: list[str] | tuple[str, ...] | None = None,
    data_labels: list[str] | tuple[str, ...] | None = None,
    plot_title: str = "TwoSubPlots",
    subplot_titles: list[str] | tuple[str, ...] | None = None,
    orientation: str = "h",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> NDArray:
    """Create two subplots arranged horizontally or vertically, with optional customization.

    Parameters
    ----------
    x_data :
        List containing x-axis data arrays for each subplot.
    y_data :
        List containing y-axis data arrays for each subplot.
    x_labels :
        List or tuple of labels for the x-axes in each subplot.
        Defaults to `[r"X$_1$", r"X$_2$"]`.
    y_labels :
        List or tuple of labels for the y-axes in each subplot.
        Defaults to `[r"Y$_1$", r"Y$_2$"]`.
    data_labels :
        List or tuple of labels for the data series in each subplot.
        Defaults to `[r"X$_1$ vs. Y$_1$", r"X$_2$ vs. Y$_2$"]`.
    plot_title :
        Title of the plot.
    subplot_titles :
        List or tuple of titles for the individual subplots, if required.
    orientation :
        Orientation of the subplots, either `'h'` for horizontal or `'v'` for vertical.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to `plt.subplots`.

    Returns
    -------
    NDArray
        A shaped `(n_rows, n_cols)` array of Matplotlib `Axes` objects.

    Raises
    ------
    DataError
        If fewer x- or y-datasets are supplied than the requested grid requires.
    OrientationError
        If `orientation` is not `'h'` or `'v'`.
    """
    _x_labels: list[str] = list(x_labels) if x_labels is not None else [r"X$_1$", r"X$_2$"]
    _y_labels: list[str] = list(y_labels) if y_labels is not None else [r"Y$_1$", r"Y$_2$"]
    _data_labels: list[str] = list(data_labels) if data_labels is not None else [r"X$_1$ vs. Y$_1$", r"X$_2$ vs. Y$_2$"]
    _subplot_titles: list[str] = list(subplot_titles) if subplot_titles is not None else ["", ""]

    if orientation in ["h", "horizontal"]:
        n_rows, n_cols = 1, 2
    elif orientation in ["v", "vertical"]:
        n_rows, n_cols = 2, 1
    else:
        raise OrientationError("The orientation must be either 'h/horizontal' or 'v/vertical'.")

    return n_plotter(
        x_data=x_data,
        y_data=y_data,
        n_rows=n_rows,
        n_cols=n_cols,
        x_labels=_x_labels,
        y_labels=_y_labels,
        data_labels=_data_labels,
        plot_title=plot_title,
        subplot_titles=_subplot_titles,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
    )


def n_plotter(
    x_data: ArrayLike | list[ArrayLike],
    y_data: ArrayLike | list[ArrayLike],
    n_rows: int,
    n_cols: int,
    x_labels: list[str] | tuple[str, ...] | None = None,
    y_labels: list[str] | tuple[str, ...] | None = None,
    data_labels: list[str] | tuple[str, ...] | None = None,
    plot_title: str | None = None,
    subplot_titles: list[str] | tuple[str, ...] | None = None,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> NDArray:
    """
    Plot multiple subplots in a grid with optional customization for each subplot.

    Parameters
    ----------
    x_data :
        List of x-axis data arrays for each subplot.
    y_data :
        List of y-axis data arrays for each subplot.
    n_rows :
        Number of rows in the subplot grid.
    n_cols :
        Number of columns in the subplot grid.
    x_labels :
        List or tuple of labels for the x-axes of each subplot.
    y_labels :
        List or tuple of labels for the y-axes of each subplot.
    data_labels :
        List or tuple of labels for the data series in each subplot.
    plot_title :
        Title of the plot.
    subplot_titles :
        List or tuple of titles for the individual subplots, if required.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default `LinePlotConfig` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to `plt.subplots`.

    Returns
    -------
    NDArray
        A shaped `(n_rows, n_cols)` array of Matplotlib `Axes` objects.

    Raises
    ------
    DataError
        If fewer x- or y-datasets are supplied than the requested grid requires.
    """
    n = n_rows * n_cols

    if len(x_data) < n:
        raise DataError(f"Grid is {n_rows}x{n_cols} ({n} panels) but only {len(x_data)} x-datasets were provided.")
    if len(y_data) < n:
        raise DataError(f"Grid is {n_rows}x{n_cols} ({n} panels) but only {len(y_data)} y-datasets were provided.")

    sp_dict = dict(figure_kwargs) if figure_kwargs else {}
    sp_dict.pop("nrows", None)
    sp_dict.pop("ncols", None)

    if isinstance(plot_config, ScatterPlotConfig) and not is_scatter:
        raise ConfigurationError(
            "`plot_config` is a `ScatterPlotConfig` but `is_scatter=False`. "
            "Set `is_scatter=True` or pass a `LinePlotConfig` instead."
        )

    if is_scatter:
        plot_items = _config_handler(input_config=plot_config, default_config=ScatterPlotConfig)
    else:
        plot_items = _config_handler(input_config=plot_config, default_config=LinePlotConfig)

    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, **sp_dict, squeeze=False)
    flat_axes = axes.flatten()

    main_dict = [
        {key: (value[c % len(value)] if isinstance(value, list) else value) for key, value in plot_items.items()}
        for c in range(n_cols * n_rows)
    ]

    _x_labels, _y_labels, _data_labels, _subplot_titles, _plot_title = _label_sanitizer(
        n_rows=n_rows,
        n_cols=n_cols,
        x_labels=x_labels,
        y_labels=y_labels,
        data_labels=data_labels,
        subplot_titles=subplot_titles,
        plot_title=plot_title,
    )

    shared_y = sp_dict.get("sharey", False)
    shared_x1 = sp_dict.get("sharex", False)
    shared_x2 = len(flat_axes) - int(len(flat_axes) / n_rows if n_rows > n_cols else n_cols)

    for index, axis, x_, y_, sp_ in zip(range(n_cols * n_rows), flat_axes, _x_labels, _y_labels, _subplot_titles):
        label = f"{_x_labels[index]} vs {_y_labels[index]}" if _data_labels is None else _data_labels[index]
        plot_or_scatter(axis=axis, scatter=is_scatter)(x_data[index], y_data[index], label=label, **main_dict[index])
        if shared_x1:
            if not index < shared_x2:
                axis.set_xlabel(x_)
        else:
            axis.set_xlabel(x_)
        if not (shared_y and index % n_cols != 0):
            axis.set_ylabel(y_)
        if label:
            axis.legend(loc="best")

        axis.set_title(sp_)

    fig.suptitle(_plot_title)

    return axes


def plot_density(
    x_data: ArrayLike,
    x_label: str = "X",
    y_label: str = "Density",
    plot_title: str = "Density Plot",
    data_label: str | None = None,
    hist_config: HistogramConfig | dict[str, Any] | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> Axes:
    """
    Plot a density histogram based on the given data and configuration.

    Parameters
    ----------
    x_data :
        The data array used for generating the density plot.
    x_label :
        The label for the x-axis.
        Default is "X".
    y_label :
        The label for the y-axis.
        Default is "Density".
    plot_title :
        The title of the density plot.
        Default is "Density Plot".
    data_label :
        The optional label for the dataset being visualized.
        Default is None.
    hist_config :
        The histogram configuration, either as an instance of `HistogramConfig`, a dictionary, or None.
        If provided, it is used to configure the histogram and ensures that `density=True` is set.
        Default is None.
    axis :
        The Matplotlib Axes object on which to draw the plot.
        If None, a new set of axes is created. Default is None.
    figure_kwargs :
        Optional keyword arguments passed when creating a new Matplotlib figure.
        These arguments are ignored if an existing axis is provided.
        Default is None.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the density plot was drawn.
    """
    if isinstance(hist_config, dict):
        if not hist_config.get("density"):
            warn(
                message="Setting `density=True` in `hist_config` for density plot.", category=UserWarning, stacklevel=2
            )
        hist_config = {**hist_config, "density": True}
    elif isinstance(hist_config, HistogramConfig):
        hist_config.density = True
    else:
        hist_config = HistogramConfig(density=True)

    return plot_hist(
        x_data=x_data,
        x_label=x_label,
        y_label=y_label,
        plot_title=plot_title,
        data_label=data_label,
        hist_config=hist_config,
        axis=axis,
        figure_kwargs=figure_kwargs,
    )


def plot_hist(
    x_data: ArrayLike,
    x_label: str = "X",
    y_label: str = "Counts",
    plot_title: str = "Histogram",
    data_label: str | None = None,
    hist_config: HistogramConfig | dict[str, Any] | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict[str, Any] | None = None,
) -> Axes:
    """
    Plot a histogram of the data.

    Parameters
    ----------
    x_data :
        Array or sequence of data points to be histogrammed.
    x_label :
        Label for the x-axis.
    y_label :
        Label for the y-axis.
    plot_title :
        Title for the plot.
    data_label :
        Label(s) for the data series. This is used in plot's legend generation.
    hist_config :
        Configuration object for histogram styling. If `None`, default configurations are used.
    axis :
        An existing matplotlib axis object on which to plot. If `None`, a new figure and axis are created.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the histogram was drawn.

    Raises
    ------
    ShapeError
        If ``x_data`` is not one-dimensional.
    """
    x = np.asarray(x_data)
    validate_1d(x, names=["x_data"])

    hist_config = _config_handler(input_config=hist_config, default_config=HistogramConfig)

    if data_label and "label" in hist_config:
        raise ConfigurationError("Both `data_label` and `hist_config['label']` cannot be provided.")

    if not hist_config.get("bins"):
        hist_config["bins"] = 32

    axis = _fig_kwargs_handler(axis=axis, fig_kwargs=figure_kwargs)
    axis.hist(x=x, label=data_label, **hist_config)

    axis.set_xlabel(x_label)
    axis.set_ylabel("Density" if hist_config.get("density") else y_label)
    axis.set_title(plot_title)

    if data_label:
        axis.legend()

    return axis


def plot_bar(
    x_data: ArrayLike,
    y_data: ArrayLike,
    plot_title: str = "Bar Plot",
    x_label: str = "X",
    y_label: str = "Y",
    bar_config: BarPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> Axes:
    """Generate a bar plot with configuration and customization options.

    Parameters
    ----------
    x_data :
        The data for the x-axis values of the bar plot.
    y_data :
        The data for the y-axis values of the bar plot.
    plot_title :
        The title of the plot, defaults to "Bar Plot".
    x_label :
        The label for the x-axis, defaults to "X".
    y_label :
        The label for the y-axis, defaults to "Y".
    bar_config :
        The configuration options for the bar plot.
        If a dictionary is provided, it will be converted to a `BarPlotConfig`.
        If not provided, a default configuration will be used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        A Matplotlib `Axes` object where the bar plot will be drawn.
        If None, a new axis will be created.

    Returns
    -------
    Axes
        The Matplotlib `Axes` object containing the bar plot.
    """
    return _bar_plot(
        x_data=x_data,
        y_data=y_data,
        x_label=x_label,
        y_label=y_label,
        plot_title=plot_title,
        figure_kwargs=figure_kwargs,
        bar_config=bar_config,
        axis=axis,
        is_bar=True,
    )


def plot_barh(
    x_data: ArrayLike,
    y_data: ArrayLike,
    plot_title: str = "Horizontal Bar Plot",
    x_label: str = "X",
    y_label: str = "Y",
    bar_config: BarPlotConfig | dict[str, Any] | None = None,
    figure_kwargs: dict[str, Any] | None = None,
    axis: Axes | None = None,
) -> Axes:
    """Generate a horizontal bar plot with configuration and customization options.

    Parameters
    ----------
    x_data :
        The category values, drawn along the y-axis (vertical positions of bars).
    y_data :
        The bar lengths (widths), drawn along the x-axis.
    plot_title :
        The title of the plot, defaults to "Horizontal Bar Plot".
    x_label :
        The label for the category axis (displayed on the y-axis).
    y_label :
        The label for the value axis (displayed on the x-axis).
    bar_config :
        The configuration options for the bar plot.
        If a dictionary is provided, it will be converted to a `BarPlotConfig`.
        If not provided, a default configuration will be used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        A Matplotlib `Axes` object where the bar plot will be drawn.
        If None, a new axis will be created.

    Returns
    -------
    Axes
        The Matplotlib `Axes` object containing the bar plot.
    """
    return _bar_plot(
        x_data=x_data,
        y_data=y_data,
        x_label=x_label,
        y_label=y_label,
        plot_title=plot_title,
        figure_kwargs=figure_kwargs,
        bar_config=bar_config,
        axis=axis,
        is_bar=False,
    )


def _bar_plot(x_data, y_data, x_label, y_label, plot_title, figure_kwargs, bar_config, axis, is_bar) -> Axes:
    x_data, y_data = np.asarray(x_data), np.asarray(y_data)

    validate_1d(x_data, y_data, names=["x_data", "y_data"])
    validate_equal_length(x_data, y_data, names=["x_data", "y_data"])

    axis = _fig_kwargs_handler(axis=axis, fig_kwargs=figure_kwargs)

    b_config = _config_handler(input_config=bar_config, default_config=BarPlotConfig)
    bar_fn = axis.bar if is_bar else axis.barh

    if any(isinstance(v, list) for v in b_config.values()):
        n = len(x_data)
        for v in b_config.values():
            if isinstance(v, list) and len(v) != n:
                warn(
                    message=f"A `bar_config` list has {len(v)} element(s) but {n} bars are being drawn. "
                    f"Values will be cycled.",
                    category=UserWarning,
                    stacklevel=3,
                )
                break
        for i, (xi, yi) in enumerate(zip(x_data, y_data)):
            bar_dict = {
                key: (value[i % len(value)] if isinstance(value, list) else value) for key, value in b_config.items()
            }
            bar_fn(xi, yi, **bar_dict)
    else:
        bar_fn(x_data, y_data, **b_config)

    if is_bar:
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
    else:
        axis.set_xlabel(y_label)
        axis.set_ylabel(x_label)
    axis.set_title(plot_title)

    return axis
