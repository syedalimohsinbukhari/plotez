"""
PlotEZ Backend Utilities.

Utility classes and functions for plot parameter management and data validation.
"""

__all__ = [
    "LinePlot",
    "ScatterPlot",
    "ErrorPlot",
    "SubPlots",
    "plot_or_scatter",
    "split_dictionary",
    "dual_axes_data_validation",
    "dual_axes_label_management",
]

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Tuple

from matplotlib.colors import Colormap, Normalize
from matplotlib.figure import Figure, SubFigure
from matplotlib.patheffects import AbstractPathEffect
from matplotlib.transforms import Affine2D, BboxBase
from numpy.typing import ArrayLike

from plotez.backend import ERROR_ATTRS, SCATTER_ATTRS
from plotez.backend.CONSTANTS import PLOT_ATTRS

# Type aliases for matplotlib types (compatible with older versions)
ColorType = Any  # str, tuple, etc.
MarkerType = Any  # str, int, etc.
label_management = Tuple[str, str, str, str, List[str]]


def _shortcuts(short_form, long_form):
    if short_form is None and long_form is None:
        return None
    return short_form if short_form else long_form


@dataclass
class _PlotParams:
    """
    Base class for handling common plot parameters.

    Parameters
    ----------
    line_style :
        Line style for the plot. Default is None.
    line_width :
        Width of the lines. Default is None.
    color :
        List or tuple containing two colors. Defaults to the first two colors in the matplotlib color cycle.
    alpha :
        Opacity of the plot elements. Default is None.
    marker :
        Marker style for the plot. Default is None.
    marker_size :
        Size of the markers. Default is None.
    marker_edge_color :
        Color of the marker edges. Default is None.
    marker_face_color :
        Color of the marker faces. Default is None.
    marker_edge_width :
        Width of the marker edges. Default is None.
    """

    agg_filter = None
    alpha: float | None = None
    animated: bool | None = None
    antialiased: bool | None = None
    clip_box: BboxBase | None = None
    clip_on: bool | Sequence[bool] | None = None
    clip_path = None
    color: ArrayLike | Sequence[ColorType] | ColorType | None = None
    dash_cap_style: str | None = None
    dash_join_style: str | None = None
    dashes: Sequence[float] | None = None
    data: ArrayLike | None = None
    draw_style: str | None = None
    figure: Figure | SubFigure | None = None
    fill_style: str | None = None
    gap_color: str | None = None
    gid: str | None = None
    in_layout: bool | None = None
    line_style: str | Sequence[str] | None = None
    line_width: float | Sequence[float] | None = None
    marker: str | MarkerType | None = None
    marker_color: str | None = None
    marker_edge_color: str | Sequence[str] | None = None
    marker_edge_width: float | Sequence[float] | None = None
    marker_face_color: str | Sequence[str] | None = None
    marker_face_color_alt: str | None = None
    marker_size: float | Sequence[float] | None = None
    mark_every: int | Sequence[int] | None = None
    mouse_over: bool | None = None
    path_effects: AbstractPathEffect | Sequence[AbstractPathEffect] | None = None
    picker: float | int | None = None
    pick_radius: float | None = None
    rasterized: bool | None = None
    sketch_parameters: dict[str, float] | None = None
    snap: bool | None = None
    solid_cap_style: str | None = None
    solid_join_style: str | None = None
    transform: Affine2D | None = None
    url: str | None = None
    visible: bool | None = None
    z_order: float | None = None

    def __post_init__(self):
        if self.marker_color:
            self.marker_face_color = self.marker_face_color if self.marker_face_color else self.marker_color
            self.marker_edge_color = self.marker_edge_color if self.marker_edge_color else self.marker_color

    def __repr__(self):
        temp_ = {label: param for label, param in zip(self._all_labels(), self._all_parameters())}
        param_str = ", ".join(f"{key}={value!r}" for key, value in temp_.items())
        return f"{self.__class__.__name__}({param_str})"

    def get_dict(self):
        """
        Get the dictionary of plot parameters, excluding None values.

        Returns
        -------
        dict
            Dictionary containing non-None parameters for the plot.
        """
        param_dict = {}

        for param, label in zip(self._all_parameters(), self._all_labels()):
            if param is not None:
                param_dict[f"{label}"] = param

        return param_dict

    def _all_parameters(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def _all_labels(self):
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class LinePlot(_PlotParams):
    """Class for double-line plot parameters."""

    def _all_parameters(self):
        return [
            self.agg_filter,
            self.alpha,
            self.animated,
            self.antialiased,
            self.clip_box,
            self.clip_on,
            self.clip_path,
            self.color,
            self.dash_cap_style,
            self.dash_join_style,
            self.dashes,
            self.data,
            self.draw_style,
            self.figure,
            self.fill_style,
            self.gap_color,
            self.gid,
            self.in_layout,
            self.line_style,
            self.line_width,
            self.marker,
            self.marker_edge_color,
            self.marker_edge_width,
            self.marker_face_color,
            self.marker_face_color_alt,
            self.marker_size,
            self.mark_every,
            self.mouse_over,
            self.path_effects,
            self.picker,
            self.pick_radius,
            self.rasterized,
            self.sketch_parameters,
            self.snap,
            self.solid_cap_style,
            self.solid_join_style,
            self.transform,
            self.url,
            self.visible,
            self.z_order,
        ]

    def _all_labels(self):
        return list(PLOT_ATTRS.keys())

    @classmethod
    def populate(cls, dictionary: Dict[str, Any]) -> "LinePlot":
        """
        Create an instance of `LinePlot` from a dictionary of parameters.

        Parameters
        ----------
        dictionary : dict
            A dictionary where keys represent parameter labels (e.g., 'ls' for line style, 'lw' for line width),
            and values represent the corresponding values for each parameter.

        Returns
        -------
        LinePlot
            An instance of `LinePlot` with attributes populated based on the provided dictionary.
        """
        instance = cls()
        for key, value in dictionary.items():
            attr_name = PLOT_ATTRS.get(key, key)
            setattr(instance, attr_name, value)

        return instance


@dataclass
class ScatterPlot(_PlotParams):
    """Class for double-scatter plot parameters."""

    size: float | None = None
    cmap: str | Colormap | None = None
    normalize: str | Normalize | None = None
    v_min: float | None = None
    v_max: float | None = None
    line_widths: float | Sequence[float] | None = None
    edge_colors: Literal["face", "none"] | ColorType | Sequence[ColorType] | None = None
    colorizer: Any | None = None
    plot_non_finite: bool | None = None

    def _all_parameters(self):
        return [
            self.size,
            self.cmap,
            self.normalize,
            self.v_min,
            self.v_max,
            self.line_widths,
            self.edge_colors,
            self.colorizer,
            self.plot_non_finite,
        ] + LinePlot()._all_parameters()

    def _all_labels(self):
        return list(SCATTER_ATTRS.keys())

    @classmethod
    def populate(cls, dictionary: Dict[str, Any]) -> "ScatterPlot":
        """
        Create an instance of `ErrorPlot` from a dictionary of parameters.

        Parameters
        ----------
        dictionary : dict
            A dictionary where keys represent parameter labels (e.g., 'ls' for line style,
            'capsize' for error bar cap size), and values represent the corresponding
            values for each parameter.

        Returns
        -------
        ErrorPlot
            An instance of `ErrorPlot` with attributes populated based on the provided dictionary.
        """
        instance = cls()
        for key, value in dictionary.items():
            attr_name = SCATTER_ATTRS.get(key, key)
            setattr(instance, attr_name, value)

        return instance


@dataclass
class ErrorPlot(LinePlot):
    """
    Class for error bar plot parameters.

    Parameters
    ----------
    capsize : float, optional
        Length of the error bar caps in points. Default is None.
    error_line_width : float, optional
        Width of the error bar lines. Default is None.
    error_color : str, optional
        Color of the error bar lines. Default is None.
    cap_thickness : float, optional
        Thickness of the error bar caps. Default is None.
    line_style : list(str), optional
        Line style for the plot. Default is None.
    line_width : list(float), optional
        Width of the lines. Default is None.
    color : list(str), optional
        Color for the error bars and line. Default is None (uses matplotlib default color cycle).
    alpha : list(float), optional
        Opacity of the plot elements. Default is None.
    marker : list(str), optional
        Marker style for the plot. Default is None.
    marker_size : list(float), optional
        Size of the markers. Default is None.
    marker_edge_color : list(str), optional
        Color of the marker edges. Default is None.
    marker_face_color : list(str), optional
        Color of the marker faces. Default is None.
    marker_edge_width : list(float), optional
        Width of the marker edges. Default is None.
    """

    error_color: str | None = None
    error_line_width: float | None = None
    capsize: float | None = None
    cap_thickness: float | None = None
    bars_above: bool | None = None
    low_lims: bool | None = None
    up_lims: bool | None = None
    x_low_lims: bool | None = None
    x_up_lims: bool | None = None
    error_every_y: int | None = None

    def _all_parameters(self):
        # Extend parent parameters with error bar specific parameters
        return [
            self.error_color,
            self.error_line_width,
            self.capsize,
            self.cap_thickness,
            self.bars_above,
            self.low_lims,
            self.up_lims,
            self.x_low_lims,
            self.x_up_lims,
            self.error_every_y,
        ] + super()._all_parameters()

    def _all_labels(self):
        return list(ERROR_ATTRS.keys())

    @classmethod
    def populate(cls, dictionary: Dict[str, Any]) -> "ErrorPlot":
        """
        Create an instance of `ErrorPlot` from a dictionary of parameters.

        Parameters
        ----------
        dictionary : dict
            A dictionary where keys represent parameter labels (e.g., 'ls' for line style,
            'capsize' for error bar cap size), and values represent the corresponding
            values for each parameter.

        Returns
        -------
        ErrorPlot
            An instance of `ErrorPlot` with attributes populated based on the provided dictionary.
        """
        instance = cls()
        for key, value in dictionary.items():
            attr_name = ERROR_ATTRS.get(key, key)
            setattr(instance, attr_name, value)

        return instance


class SubPlots(_PlotParams):
    """
    Class for subplot layouts.

    Parameters
    ----------
    share_x :
        Whether to share the x-axis across subplots. Default is False.
    share_y :
        Whether to share the y-axis across subplots. Default is False.
    fig_size :
        The size of the figure, in inches. Default is (6.4, 4.8).
    """

    def __init__(self, share_x=False, share_y=False, fig_size=None):
        super().__init__()
        self.share_x = share_x
        self.share_y = share_y
        self.fig_size = fig_size if fig_size is not None else (6.4, 4.8)

    def _all_labels(self):
        return ["sharex", "sharey", "figsize"]

    def _all_parameters(self):
        return [self.share_x, self.share_y, self.fig_size]


def plot_or_scatter(axes, scatter: bool):
    """
    Return the plot or scatter method based on the specified plot type.

    Parameters
    ----------
    axes :
        The matplotlib axis on which to apply the plot or scatter method.
    scatter :
        If True, returns the scatter method; otherwise, returns the plot method.

    Returns
    -------
    function
        The matplotlib plotting method (`axes.scatter` if scatter is True, otherwise `axes.plot`).
    """
    return axes.scatter if scatter else axes.plot


def split_dictionary(plot_instance):
    """
    Split a `LinePlot`, `ScatterPlot`, or `ErrorPlot` instance's parameters into two separate instances.

    Parameters
    ----------
    plot_instance : Union[LinePlot, ScatterPlot, ErrorPlot]
        An instance of `LinePlot`, `ScatterPlot`, or `ErrorPlot` with parameters stored as lists or tuples.
        Each parameter should be a list or tuple containing exactly two values, corresponding to settings for the
        two resulting instances.

    Returns
    -------
    Tuple[Union[LinePlot, ScatterPlot, ErrorPlot], Union[LinePlot, ScatterPlot, ErrorPlot]]
        Two instances of the same type as `plot_instance` (either `LinePlot`, `ScatterPlot`, or `ErrorPlot`),
        with parameters split based on the values in `plot_instance`.
        The first instance (`instance1`) and second instance (`instance2`) will have their attributes set according
        to the first and second elements, respectively, from each list or tuple in `plot_instance`.

    Raises
    ------
    ValueError
        If any parameter in `plot_instance` is not a list or tuple with exactly two elements.
    """
    parameters = plot_instance.get_dict()
    params_instance1, params_instance2 = {}, {}

    # Split each parameter into two separate dictionaries for the two instances
    for param_name, values in parameters.items():
        params_instance1[param_name], params_instance2[param_name] = values[:2]

    instance1 = plot_instance.__class__.populate(params_instance1)
    instance2 = plot_instance.__class__.populate(params_instance2)

    return instance1, instance2


def dual_axes_data_validation(
    x1_data: ArrayLike,
    x2_data: ArrayLike,
    y1_data: ArrayLike,
    y2_data: ArrayLike,
    use_twin_x: bool,
    axis_labels: str | list[str],
) -> None:
    """
    Validate the data and parameters for dual-axes plotting.

    Parameters
    ----------
    x1_data :
        Data for the primary x-axis.
    x2_data :
        Data for the secondary x-axis (used in dual x-axis plots). Should be `None` if `use_twin_x` is True.
    y1_data :
        Data for the primary y-axis.
    y2_data :
        Data for the secondary y-axis (used in dual y-axis plots). Should be `None` if `use_twin_x` is False.
    use_twin_x :
        If True, a dual y-axis plot is expected; otherwise, a dual x-axis plot is expected.
    axis_labels :
        List of axis labels. Must have exactly three elements:
        - Label for the x-axis of the primary plot.
        - Label for the y-axis of the primary plot.
        - Label for the secondary axis (x or y).

    Raises
    ------
    ValueError
        If any of the following conditions are met:
        - `axis_labels` does not have exactly three elements.
        - `x1_data` or `y1_data` is empty.
        - `x2_data` is provided when `use_twin_x` is True.
        - `y2_data` is provided when `use_twin_x` is False.
    """
    if len(axis_labels) != 3:
        raise ValueError("The axis_labels should have a length of 3.")
    if len(x1_data) == 0 or len(y1_data) == 0:
        raise ValueError("Primary x or y data is empty. Please provide valid data.")
    if use_twin_x and x2_data is not None:
        raise ValueError("Dual Y-axis plot requested but 'x2_data' given.")
    if not use_twin_x and y2_data is not None:
        raise ValueError("Dual X-axis plot requested but 'y2_data' given.")


def dual_axes_label_management(
    x1y1_label: str,
    x1y2_label: str,
    x2y1_label: str,
    auto_label: bool,
    axis_labels: str | Sequence[str],
    plot_title: str,
    use_twin_x: bool,
) -> label_management:
    """
    Manage labels and titles for dual-axes plots, with options for automatic labeling.

    Parameters
    ----------
    x1y1_label :
        Label for the primary plot (X1 vs. Y1).
    x1y2_label :
        Label for the secondary Y-axis plot (X1 vs. Y2), used if `use_twin_x` is True.
    x2y1_label :
        Label for the secondary X-axis plot (X2 vs. Y1), used if `use_twin_x` is False.
    auto_label :
        If True, it automatically fills in missing labels and titles with defaults.
    axis_labels :
        A list of axis labels. If provided, it must contain three strings.
        - For dual Y-axis: [primary x-axis label, primary y-axis label, secondary y-axis label].
        - For dual X-axis: [primary x-axis label, primary y-axis label, secondary x-axis label].
    plot_title :
        Title of the plot. If None and `auto_label` are True, a default title will be used.
    use_twin_x :
        If True, indicates a dual Y-axis plot (X1 vs. Y1 and X1 vs. Y2).
        If False, indicates a dual X-axis plot (X1 vs. Y1 and X2 vs. Y1).

    Returns
    -------
    Tuple[str, str, str, str, List[str]]
        A tuple containing:
        - x1y1_label: The finalized label for the primary plot.
        - x1y2_label: The finalized label for the secondary Y-axis plot.
        - x2y1_label: The finalized label for the secondary X-axis plot.
        - plot_title: The finalized plot title.
        - axis_labels: The finalized axis labels as a list of three strings.

    Notes
    -----
    - If `auto_label` is True, missing labels are replaced with default values:
        - Default axis labels:
            - Dual Y-axis: ['X', 'Y1', 'Y2']
            - Dual X-axis: ['X1', 'Y', 'X2']
        - Default data labels:
            - Dual Y-axis: ['X1 vs Y1', 'X1 vs Y2']
            - Dual X-axis: ['Y vs X1', 'X2 vs Y1']
        - Default title: 'Plot'.
    - If `auto_label` is False and labels are missing, they are replaced with empty strings.
    """
    # Set defaults for axis labels and data labels based on `use_twin_x`
    default_axis_labels = ["X", "Y1", "Y2"] if use_twin_x else ["X1", "Y", "X2"]
    default_data_labels = ["X1 vs Y1", "X1 vs Y2"] if use_twin_x else ["Y vs X1", "Y vs X2"]
    default_title = "Plot"

    if auto_label:
        # Use defaults for missing labels
        axis_labels = axis_labels or default_axis_labels
        x1y1_label = x1y1_label or default_data_labels[0]
        if use_twin_x:
            x1y2_label = x1y2_label or default_data_labels[1]
        else:
            x2y1_label = x2y1_label or default_data_labels[1]
        plot_title = plot_title or default_title
    else:
        # If auto_label is False, use provided labels or leave blank
        axis_labels = axis_labels or ["", "", ""]
        x1y1_label = x1y1_label or ""
        x1y2_label = x1y2_label or ""
        x2y1_label = x2y1_label or ""
        plot_title = plot_title or ""

    return x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels
