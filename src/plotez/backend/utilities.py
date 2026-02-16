"""
PlotEZ Backend Utilities.

Utility classes and functions for plot parameter management and data validation.
"""

__all__ = [
    "LinePlot",
    "ScatterPlot",
    "SubPlots",
    "plot_or_scatter",
    "plot_dictionary_handler",
    "split_dictionary",
    "dual_axes_data_validation",
    "dual_axes_label_management",
]

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from matplotlib import rcParams


def get_color():
    """
    Generates a list of colors from Matplotlib's default color cycle.

    This function retrieves colors from Matplotlib's default color cycle and repeats
    the cycle if more colors are needed. The user can specify the number of colors required.

    Returns
    -------
    list of str
        A list of color hex codes. The length of the list is equal to `n_colors` if specified,
        otherwise the entire extended color list is returned.

    Notes
    -----
    - The function extends the default color cycle by repeating it 10 times to accommodate
      requests for more colors than the original cycle provides.
    - If `n_colors` is greater than the original cycle length, repeated colors will appear.
    """
    color = rcParams["axes.prop_cycle"].by_key()["color"] * 10
    return color[:]


# SAFEGUARDS:
_split = Tuple[Union["LinePlot", "ScatterPlot"], Union["LinePlot", "ScatterPlot"]]
label_management = Tuple[str, str, str, str, List[str]]


class _PlotParams:
    """
    Base class for handling common plot parameters.

    Parameters
    ----------
    line_style : list(str), optional
        Line style for the plot. Default is None.
    line_width : list(float), optional
        Width of the lines. Default is None.
    color : list(str), optional
        List or tuple containing two colors. Defaults to first two colors in matplotlib color cycle.
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
    size : list(float), optional
        Size of the markers for scatter plots. Must be a list or tuple with exactly two elements. Default is None.
    cmap : list(Colormap), optional
        Colormap used for scatter plots. Default is None.
    face_color : list(str), optional
        Color of the marker faces in scatter plots. Default is None.
    """

    def __init__(
        self,
        line_style=None,
        line_width=None,
        color=None,
        alpha=None,
        marker=None,
        marker_size=None,
        marker_edge_color=None,
        marker_face_color=None,
        marker_edge_width=None,
        size=None,
        cmap=None,
        face_color=None,
    ):

        self.line_style = line_style
        self.line_width = line_width
        self.color = color
        self.alpha = alpha
        self.marker = marker
        self.marker_size = marker_size
        self.marker_edge_color = marker_edge_color
        self.marker_face_color = marker_face_color
        self.marker_edge_width = marker_edge_width

        # Additional keywords for scatter plot
        self.size = size
        self.cmap = cmap
        self.face_color = face_color

    def to_dict(self) -> dict:
        """
        Convert the plot parameters to a dictionary.

        Returns
        -------
        dict
            A dictionary where keys are parameter labels and values are the corresponding
            plot parameters. Parameters that are `None` are also included in the dictionary.
        """
        return {label: param for label, param in zip(self._all_labels(), self._all_parameters())}

    def get(self):
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


class LinePlot(_PlotParams):
    """
    Class for double-line plot parameters.

    Parameters
    ----------
    All parameters are inherited from `_PlotParams`.
    """

    def __init__(
        self,
        line_style=None,
        line_width=None,
        color=None,
        alpha=None,
        marker=None,
        marker_size=None,
        marker_edge_color=None,
        marker_face_color=None,
        marker_edge_width=None,
    ):
        super().__init__(
            line_style=line_style,
            line_width=line_width,
            color=color,
            alpha=alpha,
            marker=marker,
            marker_size=marker_size,
            marker_edge_color=marker_edge_color,
            marker_face_color=marker_face_color,
            marker_edge_width=marker_edge_width,
        )
        self.color = color or get_color()

    def __repr__(self):
        param_str = ", ".join(f"{key}={value!r}" for key, value in self.to_dict().items())
        return f"{self.__class__.__name__}({param_str})"

    def __eq__(self, other):
        if not isinstance(other, LinePlot):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __hash__(self):
        # Hash based on the tuple of sorted key-value pairs in the dictionary
        # Convert lists to tuples for hashing
        items = []
        for key, value in sorted(self.to_dict().items()):
            if isinstance(value, list):
                value = tuple(value)
            items.append((key, value))
        return hash(tuple(items))

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
            attr_name = {
                "ls": "line_style",
                "lw": "line_width",
                "color": "color",
                "alpha": "alpha",
                "marker": "marker",
                "ms": "marker_size",
                "mec": "marker_edge_color",
                "mfc": "marker_face_color",
                "mew": "marker_edge_width",
            }.get(key, key)
            setattr(instance, attr_name, value)

        return instance

    def _all_parameters(self):
        return [
            self.line_style,
            self.line_width,
            self.color,
            self.alpha,
            self.marker,
            self.marker_size,
            self.marker_edge_color,
            self.marker_face_color,
            self.marker_edge_width,
        ]

    def _all_labels(self):
        return ["ls", "lw", "color", "alpha", "marker", "ms", "mec", "mfc", "mew"]


class ScatterPlot(_PlotParams):
    """
    Class for double-scatter plot parameters.

    Parameters
    ----------
    All parameters are inherited from `_PlotParams`.
    """

    def __init__(self, color=None, alpha=None, marker=None, size=None, cmap=None, face_color=None):
        super().__init__(color=color, alpha=alpha, marker=marker, size=size, cmap=cmap, face_color=face_color)

        if self.color is None:
            self.color = color or get_color()

    def __repr__(self):
        param_str = ", ".join(f"{key}={value!r}" for key, value in self.to_dict().items())
        return f"{self.__class__.__name__}({param_str})"

    def __eq__(self, other):
        if not isinstance(other, ScatterPlot):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __hash__(self):
        # Hash based on the tuple of sorted key-value pairs in the dictionary
        # Convert lists to tuples for hashing
        items = []
        for key, value in sorted(self.to_dict().items()):
            if isinstance(value, list):
                value = tuple(value)
            items.append((key, value))
        return hash(tuple(items))

    @classmethod
    def populate(cls, dictionary: Dict[str, Any]) -> "ScatterPlot":
        """
        Create an instance of `ScatterPlot` from a dictionary of parameters.

        Parameters
        ----------
        dictionary : dict
            A dictionary where keys represent parameter labels (e.g., 's' for size, 'c' for color),
            and values represent the corresponding values for each parameter.

        Returns
        -------
        ScatterPlot
            An instance of `ScatterPlot` with attributes populated based on the provided dictionary.
        """
        instance = cls()
        for key, value in dictionary.items():
            attr_name = {
                "c": "color",
                "alpha": "alpha",
                "marker": "marker",
                "s": "size",
                "cmap": "cmap",
                "fc": "face_color",
            }.get(key, key)
            setattr(instance, attr_name, value)

        return instance

    def _all_parameters(self):
        return [self.color, self.alpha, self.marker, self.size, self.cmap, self.face_color]

    def _all_labels(self):
        return ["c", "alpha", "marker", "s", "cmap", "fc"]


class SubPlots(_PlotParams):

    def __init__(self, share_x=None, share_y=None, fig_size=None):
        super().__init__()
        self.share_x = share_x
        self.share_y = share_y
        self.fig_size = fig_size

    def _all_labels(self):
        return ["sharex", "sharey", "figsize"]

    def _all_parameters(self):
        return [self.share_x, self.share_y, self.fig_size]


def plot_or_scatter(axes, scatter: bool):
    """
    Returns the plot or scatter method based on the specified plot type.

    Parameters
    ----------
    axes : plt.axis
        The matplotlib axis on which to apply the plot or scatter method.
    scatter : bool
        If True, returns the scatter method; otherwise, returns the plot method.

    Returns
    -------
    function
        The matplotlib plotting method (`axes.scatter` if scatter is True, otherwise `axes.plot`).
    """
    return axes.scatter if scatter else axes.plot


def plot_dictionary_handler(plot_dictionary: Union[LinePlot, ScatterPlot]):
    """
    Handles plot dictionary configuration, retrieving items from the specified plot dictionary.

    If no dictionary is provided, returns items from a default LinePlot instance.

    Parameters
    ----------
    plot_dictionary : Union[LinePlot, ScatterPlot]
        The plot dictionary to retrieve items from. If None, defaults to a LinePlot instance.

    Returns
    -------
    Iterable
        An iterable of items (key-value pairs) from the specified or default plot dictionary.
    """
    return plot_dictionary.get().items() if plot_dictionary else LinePlot().get().items()


def split_dictionary(plot_instance: Union[LinePlot, ScatterPlot]) -> _split:
    """
    Split a `LinePlot` or `ScatterPlot` instance's parameters into two separate instances of the same type.

    Parameters
    ----------
    plot_instance : Union[LinePlot, ScatterPlot]
        An instance of `LinePlot` or `ScatterPlot` with parameters stored as lists or tuples of two elements.
        Each parameter should be a list or tuple containing exactly two values, corresponding to settings
        for the two resulting instances.

    Returns
    -------
    Tuple[Union[LinePlot, ScatterPlot], Union[LinePlot, ScatterPlot]]
        Two instances of the same type as `plot_instance` (either `LinePlot` or `ScatterPlot`),
        with parameters split based on the values in `plot_instance`. The first instance (`instance1`)
        and second instance (`instance2`) will have their attributes set according to the first and second
        elements, respectively, from each list or tuple in `plot_instance`.

    Raises
    ------
    ValueError
        If any parameter in `plot_instance` is not a list or tuple with exactly two elements.
    """
    # Flatten the parameters from the input plot instance
    parameters = plot_instance.get()
    params_instance1, params_instance2 = {}, {}

    # Split each parameter into two separate dictionaries for the two instances
    for param_name, values in parameters.items():
        params_instance1[param_name], params_instance2[param_name] = values[:2]

    instance1 = plot_instance.__class__.populate(params_instance1)
    instance2 = plot_instance.__class__.populate(params_instance2)

    return instance1, instance2


def dual_axes_data_validation(
    x1_data: np.ndarray,
    x2_data: Optional[np.ndarray],
    y1_data: np.ndarray,
    y2_data: Optional[np.ndarray],
    use_twin_x: bool,
    axis_labels: List[str],
) -> None:
    """
    Validates the data and parameters for dual-axes plotting.

    Parameters
    ----------
    x1_data : np.ndarray
        Data for the primary x-axis.
    x2_data : Optional[np.ndarray]
        Data for the secondary x-axis (used in dual x-axis plots). Should be `None` if `use_twin_x` is True.
    y1_data : np.ndarray
        Data for the primary y-axis.
    y2_data : Optional[np.ndarray]
        Data for the secondary y-axis (used in dual y-axis plots). Should be `None` if `use_twin_x` is False.
    use_twin_x : bool
        If True, a dual y-axis plot is expected; otherwise, a dual x-axis plot is expected.
    axis_labels : List[str]
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
    x1y1_label: Optional[str],
    x1y2_label: Optional[str],
    x2y1_label: Optional[str],
    auto_label: bool,
    axis_labels: Optional[List[str]],
    plot_title: Optional[str],
    use_twin_x: bool,
) -> label_management:
    """
    Manages labels and titles for dual-axes plots, with options for automatic labeling.

    Parameters
    ----------
    x1y1_label : Optional[str]
        Label for the primary plot (X1 vs Y1).
    x1y2_label : Optional[str]
        Label for the secondary Y-axis plot (X1 vs Y2), used if `use_twin_x` is True.
    x2y1_label : Optional[str]
        Label for the secondary X-axis plot (X2 vs Y1), used if `use_twin_x` is False.
    auto_label : bool
        If True, automatically fills in missing labels and title with defaults.
    axis_labels : Optional[List[str]]
        A list of axis labels. If provided, must contain three strings.
        - For dual Y-axis: [primary x-axis label, primary y-axis label, secondary y-axis label].
        - For dual X-axis: [primary x-axis label, primary y-axis label, secondary x-axis label].
    plot_title : Optional[str]
        Title of the plot. If None and `auto_label` is True, a default title will be used.
    use_twin_x : bool
        If True, indicates a dual Y-axis plot (X1 vs Y1 and X1 vs Y2).
        If False, indicates a dual X-axis plot (X1 vs Y1 and X2 vs Y1).

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
