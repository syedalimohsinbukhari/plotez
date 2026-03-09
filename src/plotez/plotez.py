"""
PlotEZ - Mundane plotting made easy.

This module provides simplified plotting functions for common visualization tasks.
"""

from __future__ import annotations

__all__ = [
    "plot_errorbar",
    "plot_two_column_file",
    "plot_with_dual_axes",
    "plot_xy",
    "plot_xyy",
    "plot_xxy",
    "n_plotter",
    "plot_errorband",
    "two_subplots",
]

from collections.abc import Sequence
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from numpy.typing import ArrayLike

from .backend import (
    ErrorBandConfig,
    ErrorPlotConfig,
    LinePlotConfig,
    ScatterPlotConfig,
    dual_axes_data_validation,
    dual_axes_label_management,
    plot_or_scatter,
)
from .backend.error_handling import ColumnCountError, OrientationError, ShapeError

# safeguard
lPsP = LinePlotConfig | ScatterPlotConfig
axis_return = tuple[Axes, Axes] | Axes


# =============================================================================
# Error Visualization Functions
# =============================================================================


def plot_errorband(
    x_data: ArrayLike,
    y_data: ArrayLike,
    y_lower: float | ArrayLike | None = None,
    y_upper: float | ArrayLike | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    plot_title: str | None = None,
    data_label: str | None = None,
    auto_label: bool = False,
    line: bool = True,
    band_config: ErrorBandConfig | None = None,
    line_config: LinePlotConfig | dict | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
) -> Axes | tuple[plt.Figure, Axes]:
    """
    Plot a line with an error band around it using the provided data and configurations.

    Parameters
    ----------
    x_data :
        Array or sequence containing x-coordinates for the plot.
    y_data :
        Array or sequence containing y-coordinates for the plot.
    y_lower :
        Array of absolute y-values for the lower band edge. NOT error offsets - use ``y_data - error`` if needed.
    y_upper :
        Array of absolute y-values for the upper band edge. NOT error offsets - use ``y_data + error`` if needed.
    x_label :
        Label for the x-axis. If `None`, no label will be displayed unless auto-labeling is enabled.
    y_label :
        Label for the y-axis. If `None`, no label will be displayed unless auto-labeling is enabled.
    plot_title :
        Title for the plot. If `None`, no title will be displayed unless auto-labeling is enabled.
    data_label :
        Label for the data series. This is used in legend generation if `auto_label` is enabled.
    auto_label :
        If set to `True`, default labels for axis and title are applied, and a legend is generated. Defaults to `False`.
    line : bool, optional
        If set to `True`, a central line is plotted on the graph. Defaults to `True`.
    band_config :
        Configuration object defining the style of the error band. If `None`, the default styling is applied.
    line_config :
        Configuration object defining the style of the central line. If `None`, the default styling is applied.
    figure_kwargs :
        Keyword arguments for creating the figure and axis when `axis` is not provided. Ignored if `axis` is provided.
    axis :
        An existing matplotlib axis object on which to plot. If `None`, a new figure and axis are created.

    Returns
    -------
    Axes
        A matplotlib `Axes` object containing the plot.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    if y_lower is not None:
        y_lower = np.asarray(y_lower)
    if y_upper is not None:
        y_upper = np.asarray(y_upper)

    # IDE complain hack
    f, ax = None, None
    if axis is not None:
        ax = axis
    else:
        f, ax = plt.subplots(**(figure_kwargs or {}))

    error_band_config = band_config.get_dict() if band_config else ErrorBandConfig().get_dict()
    if isinstance(line_config, dict):
        line_config = LinePlotConfig.populate(line_config)
    line_config = line_config.get_dict() if line_config else LinePlotConfig().get_dict()

    ax.fill_between(x, y_lower, y_upper, **error_band_config)

    if line:
        label = data_label or line_config.get("label") or None

        if data_label and "label" in line_config:
            warn("Both `data_label` and `line_config['label']` are provided. Using `data_label`.")

        line_config.pop("label", None)
        ax.plot(x, y, label=label, **line_config)

    ax.set_xlabel("X" if auto_label else x_label)
    ax.set_ylabel("Y" if auto_label else y_label)
    ax.set_title("ErrorBand Plot" if auto_label else plot_title)
    if auto_label or (data_label and line):
        ax.legend()

    plt.tight_layout()

    return ax if axis else (f, ax)


def plot_errorbar(
    x_data: ArrayLike,
    y_data: ArrayLike,
    x_err: float | ArrayLike | None = None,
    y_err: float | ArrayLike | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    plot_title: str | None = None,
    data_label: str | None = None,
    auto_label: bool = False,
    errorbar_config: ErrorPlotConfig | None = None,
    axis: Axes | None = None,
    figure_kwargs: dict | None = None,
) -> Axes | tuple[plt.Figure, Axes]:
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
        If `None` and `auto_label` argument is set to True, a default label "X" is used.
    y_label :
        The label for the y-axis.
        If `None` and `auto_label` argument is set to True, a default label "Y" is used.
    plot_title :
        The title of the plot.
        If `None` and `auto_label` argument is set to True, the default title "Error Bar Plot" is used.
    data_label :
        The label for the data points, which will appear in the plot legend.
        If `None`, the legend is not displayed.
    auto_label :
        If True, automatically assigns default labels for the axes and title if no labels or title are provided.
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
        The Axes object containing the error bar plot.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    if x_err is not None:
        x_err = np.asarray(x_err)
        if x_err.ndim == 2 and x_err.shape[0] != 2:
            raise ShapeError(f"Asymmetric x_err must have shape (2, N), got {x_err.shape}")

    if y_err is not None:
        y_err = np.asarray(y_err)
        if y_err.ndim == 2 and y_err.shape[0] != 2:
            raise ShapeError(f"Asymmetric y_err must have shape (2, N), got {y_err.shape}")

    # IDE complain hack
    f, ax = None, None
    if axis is not None:
        if figure_kwargs:
            warn("`figure_kwargs` is ignored when `axis` is provided.", UserWarning, stacklevel=2)
        ax = axis
    else:
        f, ax = plt.subplots(**(figure_kwargs or {}))

    errorbar_config = errorbar_config.get_dict() if errorbar_config else ErrorPlotConfig().get_dict()
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, label=data_label, **errorbar_config)

    ax.set_xlabel("X" if auto_label else x_label)
    ax.set_ylabel("Y" if auto_label else y_label)
    ax.set_title("Error Bar Plot" if auto_label else plot_title)
    if data_label:
        ax.legend()

    plt.tight_layout()

    return ax if axis else (f, ax)


# =============================================================================
# File I/O Functions
# =============================================================================


def plot_two_column_file(
    file_name: str,
    delimiter: str = ",",
    skip_header: bool = False,
    x_label: str | None = None,
    y_label: str | None = None,
    data_label: str | None = None,
    plot_title: str | None = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
    axis: Axes | None = None,
) -> axis_return:
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
    auto_label :
        If True, automatically sets the x-axis label, y-axis label, and plot title. Default is False.
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
    tuple[Axes, Axes] or Axes
        A tuple of ``(primary_axis, secondary_axis)`` if a dual-axis plot is created, otherwise a single ``Axes``.

    Raises
    ------
    ValueError
        If the file does not contain exactly two columns.
    """
    data = np.genfromtxt(file_name, delimiter=delimiter, skip_header=skip_header)

    if data.shape[1] != 2:
        raise ColumnCountError("The file must contain exactly two columns of data.")

    x_data, y_data = data.T

    return plot_xy(
        x_data=x_data,
        y_data=y_data,
        x_label=x_label,
        y_label=y_label,
        plot_title=plot_title,
        data_label=data_label,
        auto_label=auto_label,
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
    x_label: str | None = None,
    y_label: str | None = None,
    plot_title: str | None = None,
    data_label: str | None = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
    axis: Axes | None = None,
) -> axis_return:
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
        Data label for the plot to put in the legend. Defaults to 'X vs Y'.
    auto_label :
        If True, automatically sets x and y-axis labels and the plot title. Default is False.
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
    tuple[Axes, Axes] or Axes
        A tuple of ``(primary_axis, secondary_axis)`` if a dual-axis plot is created, otherwise a single ``Axes``.
    """
    if auto_label:
        x_label = "X"
        y_label = "Y"
        plot_title = "Plot"
        data_label = "X vs Y"

    axis_labels = [x_label, y_label, None]
    return plot_with_dual_axes(
        x1_data=x_data,
        y1_data=y_data,
        x1y1_label=data_label,
        auto_label=auto_label,
        axis_labels=axis_labels,
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )


# =============================================================================
# Dual-Axis Plotting Functions
# =============================================================================


def plot_xyy(
    x_data: ArrayLike,
    y1_data: ArrayLike,
    y2_data: ArrayLike,
    x_label: str | None = None,
    y1_label: str | None = None,
    y2_label: str | None = None,
    plot_title: str | None = None,
    data_labels: Sequence[str | None] = (None, None),
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
    axis: Axes | None = None,
) -> axis_return:
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
        The labels for the two datasets. Default is ``(None, None)``.
    auto_label :
        Whether to automatically label the plot. Default is `False`.
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
    tuple[Axes, Axes] or Axes
        A tuple of ``(primary_axis, secondary_axis)`` for the dual y-axis plot, or a single ``Axes``.
    """
    if auto_label:
        x_label = "X"
        y1_label = r"Y$_1$"
        y2_label = r"Y$_2$"
        plot_title = "XYY plot"
        data_labels = [r"X vs Y$_1$", r"X vs Y$_2$"]

    return plot_with_dual_axes(
        x1_data=x_data,
        y1_data=y1_data,
        y2_data=y2_data,
        x1y1_label=data_labels[0],
        x1y2_label=data_labels[1],
        use_twin_x=True,
        axis_labels=[x_label, y1_label, y2_label],
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )


def plot_xxy(
    x1_data: ArrayLike,
    x2_data: ArrayLike,
    y_data: ArrayLike,
    y_label: str | None = None,
    x1_label: str | None = None,
    x2_label: str | None = None,
    plot_title: str | None = None,
    data_labels: Sequence[str | None] = (None, None),
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
    axis: Axes | None = None,
) -> axis_return:
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
        The labels for the two datasets. Default is ``(None, None)``.
    auto_label :
        Whether to automatically label the plot. Default is `False`.
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
    tuple[Axes, Axes] or Axes
        A tuple of ``(primary_axis, secondary_axis)`` for the dual y-axis plot, or a single ``Axes``.
    """
    return plot_with_dual_axes(
        x1_data=x1_data,
        x2_data=x2_data,
        y1_data=y_data,
        x1y1_label=data_labels[0],
        x1y2_label=data_labels[1],
        use_twin_x=False,
        auto_label=auto_label,
        axis_labels=[x1_label, x2_label, y_label],
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
        axis=axis,
    )


def plot_with_dual_axes(
    x1_data: ArrayLike,
    y1_data: ArrayLike,
    x2_data: ArrayLike | None = None,
    y2_data: ArrayLike | None = None,
    x1y1_label: str | None = None,
    x1y2_label: str | None = None,
    x2y1_label: str | None = None,
    use_twin_x: bool = False,
    auto_label: bool = False,
    axis_labels: list[str] | str | None = None,
    plot_title: str | None = None,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
    axis: Axes | None = None,
) -> axis_return:
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
        If None, and `auto_label` is True, defaults to 'X1 vs Y1'.
    x1y2_label :
        Label for the plot of X1 vs. Y2 (when using dual Y-axes).
        If None, and `auto_label` is True, defaults to 'X1 vs Y2'.
    x2y1_label :
        Label for the plot of X2 vs. Y1 (when using dual X-axes).
        If None, and `auto_label` is True, defaults to 'X2 vs Y1'.
    use_twin_x :
        If True, creates a dual y-axis plot. If False, creates a dual x-axis plot. Default is False.
    auto_label :
        If True, automatically assigns labels if none are provided. Default is False.
    axis_labels :
        List of axis labels in the form [x_label, y_label1, y_label2].
        If None, and `auto_label` is True, defaults to ['X', 'Y1', 'Y2'] or ['X1', 'Y', 'X2'].
    plot_title :
        Title of the plot.
        If None, and `auto_label` is True, defaults to 'Plot'.
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
    labels = dual_axes_label_management(
        x1y1_label=x1y1_label,
        x1y2_label=x1y2_label,
        x2y1_label=x2y1_label,
        auto_label=auto_label,
        axis_labels=axis_labels,
        plot_title=plot_title,
        use_twin_x=use_twin_x,
    )

    x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = labels

    dual_axes_data_validation(
        x1_data=x1_data,
        x2_data=x2_data,
        y1_data=y1_data,
        y2_data=y2_data,
        use_twin_x=use_twin_x,
        axis_labels=axis_labels,
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
    ax1.set_xlabel(axis_labels[0])
    ax1.set_ylabel(axis_labels[1])
    if plot_title:
        ax1.set_title(plot_title)

    if use_twin_x:
        ax2 = ax1.twinx()
        if y2_data is not None:
            dict2 = {
                key: (
                    value[1]
                    if isinstance(value, list) and len(value) > 1
                    else (value[0] if isinstance(value, list) else value)
                )
                for key, value in plot_dict.items()
            }
            plot_or_scatter(axes=ax2, scatter=is_scatter)(x1_data, y2_data, label=x1y2_label, **dict2)
            ax2.set_ylabel(axis_labels[2])

    elif x2_data is not None:
        ax2 = ax1.twiny()
        dict2 = {
            key: (
                value[1]
                if isinstance(value, list) and len(value) > 1
                else (value[0] if isinstance(value, list) else value)
            )
            for key, value in plot_dict.items()
        }
        plot_or_scatter(axes=ax2, scatter=is_scatter)(x2_data, y1_data, label=x2y1_label, **dict2)
        ax2.set_xlabel(axis_labels[2])

    if x1y1_label or x1y2_label or x2y1_label:
        handles, labels = ax1.get_legend_handles_labels()
        if ax2:
            handles2, labels2 = ax2.get_legend_handles_labels()
            handles += handles2
            labels += labels2
        ax1.legend(handles, labels, loc="best")

    plt.tight_layout()

    return (ax1, ax2) if ax2 else ax1


# =============================================================================
# Multi-Panel Plotting Functions
# =============================================================================


def two_subplots(
    x_data: ArrayLike,
    y_data: ArrayLike,
    x_labels: list[str] | str | None = None,
    y_labels: list[str] | str | None = None,
    data_labels: list[str] | str | None = None,
    plot_title: str | None = None,
    subplot_title: list[str] | str | None = None,
    orientation: str = "h",
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
) -> tuple[plt.Figure, Axes]:
    """Create two subplots arranged horizontally or vertically, with optional customization.

    Parameters
    ----------
    x_data :
        List containing x-axis data arrays for each subplot.
    y_data :
        List containing y-axis data arrays for each subplot.
    x_labels :
        List of labels for the x-axes in each subplot.
    y_labels :
        List of labels for the y-axes in each subplot.
    data_labels :
        List of labels for the data series in each subplot.
    plot_title :
        Title of the plot.
    subplot_title :
        Titles for the subplots, if required.
    orientation :
        Orientation of the subplots, either ``'h'`` for horizontal or ``'v'`` for vertical.
    auto_label :
        Automatically assigns labels to subplots if `True`.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to ``plt.subplots``.

    Returns
    -------
    tuple[Figure, Axes]
        A tuple of ``(figure, axes_array)`` containing the matplotlib Figure and flattened array of Axes.

    Raises
    ------
    OrientationError
        If ``orientation`` is not ``'h'`` or ``'v'``.
    """
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
        x_labels=x_labels,
        y_labels=y_labels,
        data_labels=data_labels,
        plot_title=plot_title,
        subplot_title=subplot_title,
        auto_label=auto_label,
        is_scatter=is_scatter,
        plot_config=plot_config,
        figure_kwargs=figure_kwargs,
    )


def n_plotter(
    x_data: ArrayLike,
    y_data: ArrayLike,
    n_rows: int,
    n_cols: int,
    x_labels: str | Sequence[str] | None = None,
    y_labels: str | Sequence[str] | None = None,
    data_labels: str | Sequence[str] | None = None,
    plot_title: str | None = None,
    subplot_title: str | Sequence[str] | None = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_config: LinePlotConfig | ScatterPlotConfig | None = None,
    figure_kwargs: dict | None = None,
) -> tuple[plt.Figure, Axes]:
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
    subplot_title :
        Titles for the subplots, if required.
    auto_label :
        Automatically assigns labels to subplots if `True`.
        If `True`, it overwrites user-provided labels. Defaults to False.
    is_scatter :
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    plot_config :
        Configuration object for line or scatter styling. If None, a default ``LinePlotConfig`` is used.
    figure_kwargs :
        Keyword arguments for creating the figure and axes. Passed directly to ``plt.subplots``.

    Returns
    -------
    tuple[Figure, Axes]
        A tuple of ``(figure, axes_array)`` containing the matplotlib Figure and flattened array of Axes.
    """
    sp_dict = dict(figure_kwargs) if figure_kwargs else {}
    sp_dict.pop("nrows", None)
    sp_dict.pop("ncols", None)
    plot_items = plot_config.get_dict() if plot_config else LinePlotConfig().get_dict()  # type: ignore

    fig, axs = plt.subplots(n_rows, n_cols, **sp_dict, squeeze=False)
    axs = axs.flatten()

    main_dict = [
        {
            key: (value[c % len(value)] if isinstance(value, (list, tuple)) else value)
            for key, value in plot_items.items()
        }
        for c in range(n_cols * n_rows)
    ]

    if auto_label:
        if any([x_labels, y_labels, plot_title, subplot_title, data_labels]):
            warn("auto_label selected, it takes preference over user-provided labels.")
        x_labels = [rf"X$_{i + 1}$" for i in range(n_cols * n_rows)]
        y_labels = [rf"Y$_{i + 1}$" for i in range(n_cols * n_rows)]

        data_labels = [f"{i} vs {j}" for i, j in zip(x_labels, y_labels)]
        subplot_title = [f"Subplot {i + 1}" for i in range(n_cols * n_rows)]
        plot_title = f"{n_cols * n_rows} Plotter"
    # safeguard from `None` iterations in case if no label is provided and auto_label is false
    else:
        empty_ = [None for _ in range(n_cols * n_rows)]
        x_labels = x_labels if x_labels else empty_
        y_labels = y_labels if y_labels else empty_

        data_labels = data_labels if data_labels else empty_
        subplot_title = subplot_title if subplot_title else empty_
        plot_title = plot_title if plot_title else None

    shared_y = sp_dict.get("sharey", False)
    shared_x1 = sp_dict.get("sharex", False)
    shared_x2 = len(axs) - int(len(axs) / n_rows if n_rows > n_cols else n_cols)

    if len(x_labels) != len(y_labels):
        sm = min(len(x_labels), len(y_labels))
        lg = max(len(x_labels), len(y_labels))
        empty_ = [""] * (lg - sm)
        x_labels.extend(empty_) if len(x_labels) < lg else None
        y_labels.extend(empty_) if len(y_labels) < lg else None

        which_one = "x" if len(x_labels) < lg else "y"
        warn(
            f"The number of labels provided {which_one}_labels ({sm}) is less than the number of data series ({lg}). "
            f"Using None as missing {which_one}_label for the remaining data series."
        )

    for index, ax, x_, y_, sp_ in zip(range(n_cols * n_rows), axs, x_labels, y_labels, subplot_title):
        label = f"{x_labels[index]} vs {y_labels[index]}" if data_labels is None else data_labels[index]
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
        fig.suptitle(plot_title)

    fig.tight_layout()

    return fig, axs
