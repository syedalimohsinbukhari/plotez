"""
PlotEZ - Mundane plotting made easy.

This module provides simplified plotting functions for common visualization tasks.
"""

__all__ = [
    "plot_two_column_file",
    "plot_xy",
    "plot_xyy",
    "plot_with_dual_axes",
    "two_subplots",
    "n_plotter",
    "plot_errorbar",
]

from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from .backend import error_handling as ePl, utilities as uPl

# safeguard
plot_dictionary_type = Union[uPl.LinePlot, uPl.ScatterPlot, uPl.ErrorPlot]
axis_return = Union[Tuple[Axes, Axes], Axes]


def plot_errorbar(
    x_data,
    y_data,
    x_err=None,  # symmetric x errors, or [lower, upper] for asymmetric
    y_err=None,  # symmetric y errors, or [lower, upper] for asymmetric
    x_label=None,
    y_label=None,
    plot_title=None,
    data_label=None,
    auto_label=False,
    plot_dictionary=None,  # reuse LinePlot for line/marker styling
    errorbar_dictionary=None,  # new ErrorBar class for cap size, cap color, error line width
    subplot_dictionary=None,
    axis=None,
):
    """
    Plots data with optional error bars.

    Parameters
    ----------
    x_data : array-like
        The x-coordinates of the data points.
    y_data : array-like
        The y-coordinates of the data points.
    x_err : array-like, optional
        The error for the x-coordinates. Must have the same length as `x`.
    y_err : array-like, optional
        The error for the y-coordinates. Must have the same length as `y`.
    plot_dictionary :
        A dictionary specifying plot style options for the error bars, see LinePlot, ErrorPlot.
    subplot_dictionary : SubPlots instance, optional
        An object containing configuration options for creating subplots.
        If not provided, the default configuration from `uPl.SubPlots` will be used.
    axis : Matplotlib axis, optional
        The axis on which to plot the data.
        If not provided, a new figure and axis will be created, based on the `subplot_dictionary` configuration.
    """
    x, y = np.asarray(x_data), np.asarray(y_data)
    if x_err is not None:
        x_err = np.asarray(x_err)
    if y_err is not None:
        y_err = np.asarray(y_err)
    sp_dict = subplot_dictionary.get_dict() if subplot_dictionary else uPl.SubPlots().get_dict()
    plot_dict_items = uPl.plot_dictionary_handler(plot_dictionary=plot_dictionary)

    if not axis:
        fig, axis = plt.subplots(**sp_dict, squeeze=False)
        axis = axis.flatten()
        if isinstance(axis, np.ndarray):
            axis = axis[0]

    axis.errorbar(x, y, xerr=x_err, yerr=y_err, **plot_dict_items)
    plt.tight_layout()

    return axis


def plot_two_column_file(
    file_name: str,
    delimiter: str = ",",
    skip_header: bool = False,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    data_label: Optional[str] = None,
    plot_title: Optional[str] = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_dictionary: plot_dictionary_type = None,
    subplot_dictionary: uPl.SubPlots = None,
    axis: Optional[Axes] = None,
) -> axis_return:
    """Read a two-column file (x, y) and plot the data.

    Parameters
    ----------
    file_name : str
        The path to the file to be plotted. The file should contain two columns (x and y data).
    delimiter : str, optional
        The delimiter used in the file (default is ',').
    skip_header: bool, optional
        If True, skips the first row in the given data file, otherwise does nothing. Default is False.
    x_label: str, optional
        The label for the x-axis.
    y_label: str, optional
        The label for the y-axis.
    data_label: str, optional
        Data label for the plot to put in the legend. Defaults to 'X vs Y'.
    plot_title: str, optional
        The title for the plot.
    auto_label : bool, optional
        If True, automatically sets the x-axis label, y-axis label, and plot title. Default is False.
    is_scatter : bool, optional
        If True, creates a scatter plot. Otherwise, creates a line plot. Default is False.
    plot_dictionary: Union[LinePlot, ScatterPlot], optional
        An object representing the plot data, either a `LinePlot` or `ScatterPlot`, to be passed to the matplotlib plotting library.
         If None, a default plot type will be used.
    subplot_dictionary
        Dictionary of parameters for subplot configuration.
    axis: Optional[Axes]
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.
    """
    data = np.genfromtxt(file_name, delimiter=delimiter, skip_header=skip_header)

    if data.shape[1] != 2:
        raise ValueError("The file must contain exactly two columns of data.")

    x_data, y_data = data.T

    return plot_with_dual_axes(
        x1_data=x_data,
        y1_data=y_data,
        x1y1_label=data_label,
        auto_label=auto_label,
        axis_labels=[x_label, y_label, None],
        plot_title=plot_title,
        is_scatter=is_scatter,
        plot_dictionary=plot_dictionary,
        subplot_dictionary=subplot_dictionary,
        axis=axis,
    )


def plot_xy(
    x_data: np.ndarray,
    y_data: np.ndarray,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    plot_title: Optional[str] = None,
    data_label: Optional[str] = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_dictionary: plot_dictionary_type = None,
    subplot_dictionary: Optional[uPl.SubPlots] = None,
    axis: Optional[Axes] = None,
) -> axis_return:
    """Plot the x_data against y_data with customizable options.

    Parameters
    ----------
    x_data : np.ndarray
        The data for the x-axis.
    y_data : np.ndarray
        The data for the y-axis.
    x_label: str, optional
        The label for the x-axis.
    y_label: str, optional
        The label for the y-axis.
    plot_title: str, optional
        The title for the plot.
    data_label: str, optional
        Data label for the plot to put in the legend. Defaults to 'X vs Y'.
    auto_label : bool, optional
        If True, automatically sets x and y-axis labels and the plot title. Default is False.
    is_scatter : bool, optional
        If True, creates a scatter plot. Otherwise, creates a line plot. Default is False.
    plot_dictionary: Union[LinePlot, ScatterPlot], optional
        An object representing the plot data, either a `LinePlot` or `ScatterPlot`,  to be passed to the matplotlib plotting library.
        If None, a default plot type will be used.
    subplot_dictionary: SubPlots, optional
        Dictionary of parameters for subplot configuration.
    axis: Optional[Axes]
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.
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
        plot_dictionary=plot_dictionary,
        subplot_dictionary=subplot_dictionary,
        axis=axis,
    )


def plot_xyy(
    x_data: np.ndarray,
    y1_data: np.ndarray,
    y2_data: np.ndarray,
    x_label: Optional[str] = None,
    y1_label: Optional[str] = None,
    y2_label: Optional[str] = None,
    plot_title: Optional[str] = None,
    data_labels: Optional[List[str]] = (None, None),
    use_twin_x: bool = True,
    auto_label: bool = False,
    is_scatter: bool = False,
    plot_dictionary: plot_dictionary_type = None,
    subplot_dictionary: Optional[uPl.SubPlots] = None,
    axis=None,
) -> axis_return:
    """Plot two sets of y-data (`y1_data` and `y2_data`) against the same x-data (`x_data`) on the same plot.

    Parameters
    ----------
    x_data : np.ndarray
        The x-axis data for both plots.
    y1_data : np.ndarray
        The first set of y-axis data to be plotted against `x_data`.
    y2_data : np.ndarray
        The second set of y-axis data to be plotted against `x_data`.
    x_label: str
        The label for the x-axis.
    y1_label: str
        The label for the first y-axis.
    y2_label: str
        The label for the second y-axis.
    plot_title: str
        The title for the plot.
    data_labels : list of str, optional
        The labels for the two datasets. Default is `['X vs Y1', 'X vs Y2']`.
    use_twin_x : bool, optional
        If True, creates dual y-axis plot. If False, creates dual x-axis plot. Default is True.
    auto_label : bool, optional
        Whether to automatically label the plot. Default is `False`.
    is_scatter : bool, optional
        Whether to create a scatter plot (`True`) or a line plot (`False`). Default is `False`.
    plot_dictionary: Union[LinePlot, ScatterPlot], optional
        An object representing the plot data, either a `LinePlot` or `ScatterPlot`, to be passed to the matplotlib plotting library.
    subplot_dictionary: SubPlots
        Dictionary of parameters for subplot configuration.
    axis : Axes, optional
        A Matplotlib axis to plot on. If `None`, a new axis is created. Default is `None`.
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
        auto_label=auto_label,
        plot_title=plot_title,
        use_twin_x=use_twin_x,
        axis_labels=[x_label, y1_label, y2_label],
        is_scatter=is_scatter,
        plot_dictionary=plot_dictionary,
        subplot_dictionary=subplot_dictionary,
        axis=axis,
    )


def plot_with_dual_axes(
    x1_data: np.ndarray,
    y1_data: np.ndarray,
    x2_data: np.ndarray = None,
    y2_data: np.ndarray = None,
    x1y1_label: Optional[str] = None,
    x1y2_label: Optional[str] = None,
    x2y1_label: Optional[str] = None,
    use_twin_x: bool = False,
    auto_label: bool = False,
    axis_labels: Optional[List[str]] = None,
    plot_title: Optional[str] = None,
    is_scatter: bool = False,
    plot_dictionary: plot_dictionary_type = None,
    subplot_dictionary: Optional[uPl.SubPlots] = None,
    axis: Optional[Axes] = None,
) -> axis_return:
    """Plot the data with options for dual axes (x or y) or single axis.

    Parameters
    ----------
    x1_data : np.ndarray
        Data for the primary x-axis.
    y1_data : np.ndarray
        Data for the primary y-axis.
    x2_data : np.ndarray, optional
        Data for the secondary x-axis (used for dual x-axis plots).
    y2_data : np.ndarray, optional
        Data for the secondary y-axis (used for dual y-axis plots).
    x1y1_label : str, optional
        Label for the plot of X1 vs Y1. If None and `auto_label` is True, defaults to 'X1 vs Y1'.
    x1y2_label : str, optional
        Label for the plot of X1 vs Y2 (when using dual Y-axes). If None and `auto_label` is True, defaults to 'X1 vs Y2'.
    x2y1_label : str, optional
        Label for the plot of X2 vs Y1 (when using dual X-axes). If None and `auto_label` is True, defaults to 'X2 vs Y1'.
    use_twin_x : bool, optional
        If True, creates dual y-axis plot. If False, creates dual x-axis plot. Default is False.
    auto_label : bool, optional
        If True, automatically assigns labels if none are provided. Default is False.
    axis_labels : list of str, optional
        List of axis labels in the form [x_label, y_label1, y_label2].
        If None and `auto_label` is True, defaults to ['X', 'Y1', 'Y2'] or ['X1', 'Y', 'X2'].
    plot_title : str, optional
        Title of the plot. If None and `auto_label` is True, defaults to 'Plot'. If None and `auto_label` is False, no title is added.
    is_scatter : bool, optional
        If True, creates scatter plot; otherwise, line plot. Default is False.
    plot_dictionary: Union[LinePlot, ScatterPlot], optional
        An object representing the plot data, either a `LinePlot` or `ScatterPlot`, to be passed to the matplotlib plotting library.
    subplot_dictionary: SubPlots
        Dictionary of parameters for subplot configuration.
    axis: Optional[Axis]
        The axis object to draw the plots on. If not passed, a new axis object will be created internally.
    """
    labels = uPl.dual_axes_label_management(
        x1y1_label=x1y1_label,
        x1y2_label=x1y2_label,
        x2y1_label=x2y1_label,
        auto_label=auto_label,
        axis_labels=axis_labels,
        plot_title=plot_title,
        use_twin_x=use_twin_x,
    )

    x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels = labels

    uPl.dual_axes_data_validation(
        x1_data=x1_data,
        x2_data=x2_data,
        y1_data=y1_data,
        y2_data=y2_data,
        use_twin_x=use_twin_x,
        axis_labels=axis_labels,
    )

    if axis:
        ax1 = axis
    else:
        sp_dict = subplot_dictionary.get_dict() if subplot_dictionary else uPl.SubPlots().get_dict()
        _, ax1 = plt.subplots(1, 1, **sp_dict)

    plot_items = uPl.plot_dictionary_handler(plot_dictionary=plot_dictionary)
    dict1 = {key: (value[0] if isinstance(value, list) else value) for key, value in plot_items.items()}
    uPl.plot_or_scatter(axes=ax1, scatter=is_scatter)(x1_data, y1_data, label=x1y1_label, **dict1)

    ax2 = None
    ax1.set_xlabel(axis_labels[0])
    ax1.set_ylabel(axis_labels[1])
    if plot_title:
        ax1.set_title(plot_title)

    if use_twin_x:
        ax2 = ax1.twinx()
        if y2_data is not None:
            dict2 = {key: (value[1] if len(value) > 1 else value[0]) for key, value in plot_items.items()}
            uPl.plot_or_scatter(axes=ax2, scatter=is_scatter)(x1_data, y2_data, label=x1y2_label, **dict2)
            ax2.set_ylabel(axis_labels[2])

    elif x2_data is not None:
        ax2 = ax1.twiny()
        dict2 = {key: (value[1] if len(value) > 1 else value[0]) for key, value in plot_items.items()}
        uPl.plot_or_scatter(axes=ax2, scatter=is_scatter)(x2_data, y1_data, label=x2y1_label, **dict2)
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


def two_subplots(
    x_data: List[np.ndarray],
    y_data: List[np.ndarray],
    x_labels: Optional[List[str]] = None,
    y_labels: Optional[List[str]] = None,
    data_labels: Optional[List[str]] = None,
    plot_title: Optional[str] = None,
    subplot_title: Optional[List[str]] = None,
    orientation: str = "h",
    auto_label: bool = False,
    is_scatter: bool = False,
    subplot_dictionary: Optional[uPl.SubPlots] = None,
    plot_dictionary: Optional[Union[uPl.LinePlot, uPl.ScatterPlot]] = None,
) -> Tuple[plt.Figure, np.ndarray]:
    """Create two subplots arranged horizontally or vertically, with optional customization.

    Parameters
    ----------
    x_data : list of np.ndarray
        List containing x-axis data arrays for each subplot.
    y_data : list of np.ndarray
        List containing y-axis data arrays for each subplot.
    x_labels : list of str
        List of labels for the x-axes in each subplot.
    y_labels : list of str
        List of labels for the y-axes in each subplot.
    data_labels : list of str
        List of labels for the data series in each subplot.
    plot_title: str, optional
        Title of the plot.
    subplot_title: list of str, optional
        Titles for the subplots, if required.
    orientation : str, optional, default='h'
        Orientation of the subplots, either 'h' for horizontal or 'v' for vertical.
    auto_label : bool, default False
        Automatically assigns labels to subplots if `True`.
    is_scatter : bool, default False
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    subplot_dictionary : dict, optional
        Dictionary of parameters for subplot configuration.
    plot_dictionary : LinePlot or ScatterPlot, optional
        Object containing plot styling parameters. Defaults to `LinePlot`.
    """
    if orientation == "h":
        n_rows, n_cols = 1, 2
    elif orientation == "v":
        n_rows, n_cols = 2, 1
    else:
        raise ePl.OrientationError("The orientation must be either 'h' or 'v'.")

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
        subplot_dictionary=subplot_dictionary,
        plot_dictionary=plot_dictionary,
    )


def n_plotter(
    x_data: List[np.ndarray],
    y_data: List[np.ndarray],
    n_rows: int,
    n_cols: int,
    x_labels: Optional[List[str]] = None,
    y_labels: Optional[List[str]] = None,
    data_labels: Optional[List[str]] = None,
    plot_title: Optional[str] = None,
    subplot_title: Optional[List[str]] = None,
    auto_label: bool = False,
    is_scatter: bool = False,
    subplot_dictionary: Optional[uPl.SubPlots] = None,
    plot_dictionary: Optional[Union[uPl.LinePlot, uPl.ScatterPlot]] = None,
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Plot multiple subplots in a grid with optional customization for each subplot.

    Parameters
    ----------
    x_data : list of np.ndarray
        List of x-axis data arrays for each subplot.
    y_data : list of np.ndarray
        List of y-axis data arrays for each subplot.
    n_rows : int
        Number of rows in the subplot grid.
    n_cols : int
        Number of columns in the subplot grid.
    x_labels : list of str, optional
        List of labels for the x-axes of each subplot.
    y_labels : list of str, optional
        List of labels for the y-axes of each subplot.
    data_labels : list of str, optional
        List of labels for the data series in each subplot.
    plot_title: str, optional
        Title of the plot.
    subplot_title: list of str, optional
        Titles for the subplots, if required.
    auto_label : bool, default False
        Automatically assigns labels to subplots if `True`. If `True`, it overwrites user provided labels. Defaults to False.
    is_scatter : bool, default False
        If `True`, plots data as scatter plots; otherwise, plots as line plots.
    subplot_dictionary : dict, optional
        Dictionary of parameters for subplot configuration.
    plot_dictionary : LinePlot or ScatterPlot, optional
        Object containing plot styling parameters. Defaults to `LinePlot`.
    """
    sp_dict = subplot_dictionary.get_dict() if subplot_dictionary else uPl.SubPlots().get_dict()

    fig, axs = plt.subplots(n_rows, n_cols, **sp_dict, squeeze=False)
    axs = axs.flatten()

    plot_items = uPl.plot_dictionary_handler(plot_dictionary=plot_dictionary)

    main_dict = [{key: value[c % len(value)] for key, value in plot_items.items()} for c in range(n_cols * n_rows)]

    if auto_label:
        x_labels = [rf"X$_{i + 1}$" for i in range(n_cols * n_rows)]
        y_labels = [rf"Y$_{i + 1}$" for i in range(n_cols * n_rows)]

        data_labels = [f"{i} vs {j}" for i, j in zip(x_labels, y_labels)]
        subplot_title = [f"Subplot {i}" for i in range(n_cols * n_rows)]
        plot_title = f"{n_cols * n_rows} Plotter"
    # safeguard from `None` iterations in case if no label is provided and auto_label is false
    else:
        empty_ = [None for _ in range(n_cols * n_rows)]
        x_labels = x_labels if x_labels else empty_
        y_labels = y_labels if y_labels else empty_
        plot_title = plot_title if plot_title else None
        data_labels = data_labels if data_labels else empty_
        subplot_title = subplot_title if subplot_title else empty_

    shared_y = sp_dict.get("sharey")
    shared_x1 = sp_dict.get("sharex")
    shared_x2 = len(axs) - int(len(axs) / n_rows if n_rows > n_cols else n_cols)

    for index, ax, x_, y_, sp_ in zip(range(n_cols * n_rows), axs, x_labels, y_labels, subplot_title):
        label = f"{x_labels[index]} vs {y_labels[index]}" if data_labels is None else data_labels[index]
        uPl.plot_or_scatter(axes=ax, scatter=is_scatter)(x_data[index], y_data[index], label=label, **main_dict[index])
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
