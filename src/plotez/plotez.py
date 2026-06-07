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
]

from warnings import warn

import matplotlib.pyplot as plt
import numpy as np

from .backend import (
    ErrorBandConfig,
    ErrorPlotConfig,
    HistogramConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    dual_axes_data_validation,
    plot_or_scatter,
)
from .backend.error_handling import ColumnCountError, ConfigurationError, OrientationError, ShapeError
from .typing import ArrayLike, Axes, AxesReturn, NDArray

# =============================================================================
# Error Visualization Functions
# =============================================================================


def plot_errorband_relative(
    x_data: ArrayLike,
    y_data: ArrayLike,
    y_lower: int | float | ArrayLike | None = None,
    y_upper: int | float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBand",
    data_label: str = "X vs. Y",
    line: bool = True,
    band_config: ErrorBandConfig | None = None,
    line_config: LinePlotConfig | dict | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
) -> Axes:
    """
    Plot a line graph with a shaded error band using relative (offset) errors.

    A convenience wrapper around :func:`plot_errorband` where ``y_lower`` and ``y_upper`` are interpreted as offsets
    from ``y_data`` rather than absolute bounds.
    Internally, the absolute bounds are computed as ``y_data - y_lower`` and ``y_data + y_upper`` before passing
    to :func:`plot_errorband`.

    Parameters
    ----------
    x_data :
        The independent variable values to plot.
    y_data :
        The central values to plot.
    y_lower :
        The downward offset from ``y_data`` defining the lower band edge.
        If ``None``, it is inferred as equal to ``y_upper``, implying a symmetric band.
        At least one of ``y_lower`` or ``y_upper`` must be provided.
    y_upper :
        The upward offset from ``y_data`` defining the upper band edge.
        If ``None``, it is inferred as equal to ``y_lower``, implying a symmetric band.
        At least one of ``y_lower`` or ``y_upper`` must be provided.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title of the plot.
    data_label :
        The label for the data series, used in the legend.
        If ``line=True``, the label is attached to the line.
        If ``line=False``, it is attached to the band.
    line :
        Whether to draw a line through the central values over the error band.
    band_config :
        Configuration for the error band styling.
        If ``None``, defaults are used.
    line_config :
        Configuration for the line styling.
        If ``None``, defaults are used.
    axis :
        Pre-existing Matplotlib axes to draw on.
        If provided, ``figure_kwargs`` is ignored.
    figure_kwargs :
        Keyword arguments passed to ``plt.subplots`` when creating a new figure.
        Ignored if ``axis`` is provided.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.

    Raises
    ------
    ConfigurationError
        If both ``y_lower`` and ``y_upper`` are ``None``.

    See Also
    --------
    plot_errorband : The absolute-bounds version of this function.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    return plot_errorband(
        x_data=x,
        y_data=y,
        y_lower=(y - np.asarray(y_lower)) if y_lower is not None else None,
        y_upper=(y + np.asarray(y_upper)) if y_upper is not None else None,
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
    y_lower: int | float | ArrayLike | None = None,
    y_upper: int | float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBand",
    data_label: str = "X vs. Y",
    line: bool = True,
    band_config: ErrorBandConfig | None = None,
    line_config: LinePlotConfig | dict | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
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
        If ``None``, it is inferred as a symmetric reflection of ``y_upper`` through ``y_data``.
        At least one of ``y_lower`` or ``y_upper`` must be provided.
    y_upper :
        The upper bound of the error band.
        If ``None``, it is inferred as a symmetric reflection of ``y_lower`` through ``y_data``.
        At least one of ``y_lower`` or ``y_upper`` must be provided.
    x_label :
        The label for the x-axis.
    y_label :
        The label for the y-axis.
    plot_title :
        The title of the plot.
    data_label :
        The label for the data series, used in the legend.
        If ``line=True``, the label is attached to the line.
        If ``line=False``, it is attached to the band.
    line :
        Whether to draw a line through the central values over the error band.
    band_config :
        Configuration for the error band styling.
        If ``None``, defaults are used.
    line_config :
        Configuration for the line styling.
        If ``None``, defaults are used.
    axis :
        Pre-existing Matplotlib axes to draw on.
        If provided, ``figure_kwargs`` is ignored.
    figure_kwargs :
        Keyword arguments passed to ``plt.subplots`` when creating a new figure.
        Ignored if ``axis`` is provided.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.

    Raises
    ------
    ConfigurationError
        If both ``y_lower`` and ``y_upper`` are ``None``.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)

    if y_lower is None and y_upper is None:
        raise ConfigurationError("At least one of `y_lower` or `y_upper` must be provided for the error band.")

    if y_lower is not None:
        y_lower = np.asarray(y_lower)
    if y_upper is not None:
        y_upper = np.asarray(y_upper)

    if y_lower is None:
        y_lower = y - (y_upper - y)
    elif y_upper is None:
        y_upper = y + (y - y_lower)

    if axis is not None:
        ax = axis
        if figure_kwargs:
            warn(message="`figure_kwargs` is ignored when `axis` is provided.", category=UserWarning, stacklevel=2)
    else:
        _, ax = plt.subplots(**(figure_kwargs or {}))

    error_band_config = band_config.get_dict() if band_config else ErrorBandConfig().get_dict()
    if isinstance(line_config, dict):
        line_config: LinePlotConfig = LinePlotConfig.populate(line_config)
    l_conf = line_config.get_dict() if line_config else LinePlotConfig().get_dict()

    if line:
        _data_label = data_label or l_conf.get("label") or None

        if data_label and "label" in l_conf:
            warn("Both `data_label` and `line_config['label']` are provided. Using `data_label`.")

            l_conf.pop("label", None)

        ax.fill_between(x=x, y1=y_lower, y2=y_upper, **error_band_config)
        ax.plot(x, y, label=_data_label, **l_conf)
    else:
        ax.fill_between(x=x, y1=y_lower, y2=y_upper, label=data_label, **error_band_config)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(plot_title)
    ax.legend()

    return ax


def plot_errorbar(
    x_data: ArrayLike,
    y_data: ArrayLike,
    x_err: int | float | ArrayLike | None = None,
    y_err: int | float | ArrayLike | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    plot_title: str = "XY ErrorBar",
    data_label: str = "X vs. Y",
    errorbar_config: ErrorPlotConfig | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
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
        If `None`, a new subplot is created using ``figure_kwargs``.

    Returns
    -------
    Axes
        The Matplotlib Axes on which the plot was drawn.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    if x_err is not None:
        x_err: NDArray = np.asarray(x_err)
        if x_err.ndim == 2 and x_err.shape[0] != 2:
            raise ShapeError(f"Asymmetric x_err must have shape (2, N), got {x_err.shape}")

    if y_err is not None:
        y_err: NDArray = np.asarray(y_err)
        if y_err.ndim == 2 and y_err.shape[0] != 2:
            raise ShapeError(f"Asymmetric y_err must have shape (2, N), got {y_err.shape}")

    if axis is not None:
        if figure_kwargs:
            warn(message="`figure_kwargs` is ignored when `axis` is provided.", category=UserWarning, stacklevel=2)
        ax = axis
    else:
        _, ax = plt.subplots(**(figure_kwargs or {}))

    ebc = errorbar_config.get_dict() if errorbar_config else ErrorPlotConfig().get_dict()
    ax.errorbar(x=x, y=y, xerr=x_err, yerr=y_err, label=data_label, **ebc)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(plot_title)
    ax.legend()

    return ax


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
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
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
    ColumnCountError
        If the file does not contain exactly two columns.
    """
    data = np.genfromtxt(fname=file_name, delimiter=delimiter, skip_header=skip_header)

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
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        If True, creates a scatter plot. Otherwise, creates a line plot. Default is False.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.

    Returns
    -------
    Axes
        The axes object of the plot.
    """
    _axis = plot_with_dual_axes(
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

    _axis: Axes
    return _axis


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
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        The labels for the two datasets. Default is ``(r"X vs. Y$_1$", r"X vs. Y$_2$")``.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    is_scatter :
        Whether to create a scatter plot (`True`) or a line plot (`False`). Default is `False`.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        A Matplotlib axis to plot on. If `None`, a new axis is created. Default is `None`.

    Returns
    -------
    tuple[Axes, Axes]
        A tuple of ``(primary_axis, secondary_axis)`` for the dual y-axis plot.
    """
    _data_labels: list[str] = list(data_labels) if data_labels is not None else [r"X vs. Y$_1$", r"X vs. Y$_2$"]

    _axis = plot_with_dual_axes(
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

    _axis: tuple[Axes, Axes]
    return _axis


def plot_xxy(
    x1_data: ArrayLike,
    x2_data: ArrayLike,
    y_data: ArrayLike,
    y_label: str = "Y",
    x1_label: str = r"X$_1$",
    x2_label: str = r"X$_2$",
    data_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    plot_title: str = "",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        The labels for the two datasets. Default is ``(r"Y vs. X$_1$", r"Y vs. X$_2$")``.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    is_scatter :
        Whether to create a scatter plot (`True`) or a line plot (`False`). Default is `False`.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        A Matplotlib axis to plot on. If `None`, a new axis is created. Default is `None`.

    Returns
    -------
    tuple[Axes, Axes]
        A tuple of ``(primary_axis, secondary_axis)`` for the dual x-axis plot.
    """
    _data_labels: list[str] = list(data_labels) if data_labels is not None else [r"Y vs. X$_1$", r"Y vs. X$_2$"]

    _axis = plot_with_dual_axes(
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

    _axis: tuple[Axes, Axes]
    return _axis


def plot_with_dual_axes(
    x1_data: ArrayLike,
    y1_data: ArrayLike,
    x2_data: ArrayLike | None = None,
    y2_data: ArrayLike | None = None,
    x1y1_label: str = r"X$_1$ vs. Y$_1$",
    x1y2_label: str = r"X$_1$ vs. Y$_2$",
    x2y1_label: str = r"X$_2$ vs. Y$_1$",
    use_twin_x: bool = False,
    axis_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    plot_title: str = "DualAxesPlot",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        List of axis labels in the form ``[x_label, y_label1, y_label2]``.
        Defaults to ``["X", r"Y$_1$", r"Y$_2$"]`` when not provided.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    plot_title :
        Title of the plot.
    is_scatter :
        If True, creates scatter plot; otherwise, line plot. Default is False.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.

    Returns
    -------
    tuple[Axes, Axes] or Axes
        A tuple of ``(primary_axis, secondary_axis)`` when dual axes are used, otherwise a single ``Axes``.
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
        plot_dict = LinePlotConfig().get_dict()

    dict1 = {key: (value[0] if isinstance(value, list) else value) for key, value in plot_dict.items()}
    plot_or_scatter(axes=ax1, scatter=is_scatter)(x1_data, y1_data, label=x1y1_label, **dict1)

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
        if y2_data is not None:
            plot_or_scatter(axes=ax2, scatter=is_scatter)(x1_data, y2_data, label=x1y2_label, **dict2)
            ax2.set_ylabel(_axis_labels[2])

    elif x2_data is not None:
        ax2 = ax1.twiny()
        plot_or_scatter(axes=ax2, scatter=is_scatter)(x2_data, y1_data, label=x2y1_label, **dict2)
        ax2.set_xlabel(_axis_labels[2])

    if x1y1_label or x1y2_label or x2y1_label:
        handles, labels = ax1.get_legend_handles_labels()
        if ax2:
            handles2, labels2 = ax2.get_legend_handles_labels()
            handles += handles2
            labels += labels2
        ax1.legend(handles, labels, loc="best")

    return (ax1, ax2) if ax2 else ax1


# =============================================================================
# Multi-Panel Plotting Functions
# =============================================================================


def two_subplots(
    x_data: ArrayLike | list[ArrayLike],
    y_data: ArrayLike | list[ArrayLike],
    x_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    y_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    data_labels: list[str] | tuple[str, ...] | None = None,  # noqa
    plot_title: str = "TwoSubPlots",
    subplot_titles: list[str] | tuple[str, ...] | None = None,  # noqa
    orientation: str = "h",
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
) -> NDArray:
    """Create two subplots arranged horizontally or vertically, with optional customization.

    Parameters
    ----------
    x_data :
        List containing x-axis data arrays for each subplot.
    y_data :
        List containing y-axis data arrays for each subplot.
    x_labels :
        List of labels for the x-axes in each subplot.
        Defaults to ``[r"X$_1$", r"X$_2$"]``.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    y_labels :
        List of labels for the y-axes in each subplot.
        Defaults to ``[r"Y$_1$", r"Y$_2$"]``.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    data_labels :
        List of labels for the data series in each subplot.
        Defaults to ``[r"X$_1$ vs. Y$_1$", r"X$_2$ vs. Y$_2$"]``.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    plot_title :
        Title of the plot.
    subplot_titles :
        Titles for the individual subplots, if required.
        Passing a mutable ``list`` is deprecated; use a ``tuple`` instead.
    orientation :
        Orientation of the subplots, either ``'h'`` for horizontal or ``'v'`` for vertical.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to ``plt.subplots``.

    Returns
    -------
    NDArray
        A shaped ``(n_rows, n_cols)`` array of Matplotlib ``Axes`` objects.

    Raises
    ------
    OrientationError
        If ``orientation`` is not ``'h'`` or ``'v'``.
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


def _label_sanitizer(
    n_rows: int,
    n_cols: int,
    x_labels: list[str] | None,
    y_labels: list[str] | None,
    data_labels: list[str] | None,
    subplot_titles: list[str] | None,
    plot_title: str | None,
) -> tuple[list[str], list[str], list[str], list[str], str]:
    n = n_rows * n_cols

    def _pad(labels: list[str] | None, name: str) -> list[str]:
        if labels is None:
            return [""] * n
        if len(labels) < n:
            warn(
                message=f"`{name}` has {len(labels)} element(s) but a {n_rows}×{n_cols} grid ({n} subplots) was "
                f"requested. Padding with empty strings for the remaining {n - len(labels)}.",
                category=UserWarning,
                stacklevel=3,
            )
            return labels + [""] * (n - len(labels))
        if len(labels) > n:
            warn(
                message=f"`{name}` has {len(labels)} element(s) but a {n_rows}×{n_cols} grid "
                f"({n} subplots) was requested. Trimming the last {len(labels) - n} element(s).",
                category=UserWarning,
                stacklevel=3,
            )
            return labels[:n]
        return labels

    return (
        _pad(labels=x_labels, name="x_labels"),
        _pad(labels=y_labels, name="y_labels"),
        _pad(labels=data_labels, name="data_labels"),
        _pad(labels=subplot_titles, name="subplot_titles"),
        plot_title or "",
    )


def n_plotter(
    x_data: ArrayLike | list[ArrayLike],
    y_data: ArrayLike | list[ArrayLike],
    n_rows: int,
    n_cols: int,
    x_labels: list[str] | None = None,
    y_labels: list[str] | None = None,
    data_labels: list[str] | None = None,
    plot_title: str | None = None,
    subplot_titles: list[str] | None = None,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
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
        List of labels for the x-axes of each subplot.
    y_labels :
        List of labels for the y-axes of each subplot.
    data_labels :
        List of labels for the data series in each subplot.
    plot_title :
        Title of the plot.
    subplot_titles :
        Titles for the individual subplots, if required.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to ``plt.subplots``.

    Returns
    -------
    NDArray
        A shaped ``(n_rows, n_cols)`` array of Matplotlib ``Axes`` objects.
    """
    sp_dict = dict(figure_kwargs) if figure_kwargs else {}
    sp_dict.pop("nrows", None)
    sp_dict.pop("ncols", None)

    if isinstance(plot_config, ScatterPlotConfig) and not is_scatter:
        raise ConfigurationError(
            "`plot_config` is a `ScatterPlotConfig` but `is_scatter=False`. "
            "Set `is_scatter=True` or pass a `LinePlotConfig` instead."
        )

    plot_items = plot_config.get_dict() if plot_config else LinePlotConfig().get_dict()  # type: ignore

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, **sp_dict, squeeze=False)
    flat_axs = axs.flatten()

    main_dict = [
        {
            key: (value[c % len(value)] if isinstance(value, (list, tuple)) else value)
            for key, value in plot_items.items()
        }
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
    shared_x2 = len(flat_axs) - int(len(flat_axs) / n_rows if n_rows > n_cols else n_cols)

    for index, ax, x_, y_, sp_ in zip(range(n_cols * n_rows), flat_axs, _x_labels, _y_labels, _subplot_titles):
        label = f"{_x_labels[index]} vs {_y_labels[index]}" if _data_labels is None else _data_labels[index]
        plot_or_scatter(axes=ax, scatter=is_scatter)(x_data[index], y_data[index], label=label, **main_dict[index])
        if shared_x1:
            if not index < shared_x2:
                ax.set_xlabel(x_)
        else:
            ax.set_xlabel(x_)
        if not (shared_y and index % n_cols != 0):
            ax.set_ylabel(y_)
        if label:
            ax.legend(loc="best")

        ax.set_title(sp_)

    fig.suptitle(_plot_title)

    return axs


def plot_density(
    x_data: ArrayLike,
    x_label: str = "X",
    y_label: str = "Density",
    plot_title: str = "Density Plot",
    data_label: str | None = None,
    hist_config: HistogramConfig | dict | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
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
    hist_config: HistogramConfig | dict | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
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
    """
    x = np.asarray(x_data)
    if isinstance(hist_config, dict):
        h_config = HistogramConfig.populate(hist_config).get_dict()
    elif isinstance(hist_config, HistogramConfig):
        h_config = hist_config.get_dict()
    else:
        h_config = HistogramConfig().get_dict()

    if axis is not None:
        ax = axis
    else:
        _, ax = plt.subplots(**(figure_kwargs or {}))

    if data_label and "label" in h_config:
        raise ConfigurationError("Both `data_label` and `hist_config['label']` cannot be provided.")

    if not h_config.get("bins"):
        h_config["bins"] = 32

    ax.hist(x=x, label=data_label, **h_config)

    ax.set_xlabel(x_label)
    ax.set_ylabel("Density" if h_config.get("density") else y_label)
    ax.set_title(plot_title)

    if data_label:
        ax.legend()

    return ax
