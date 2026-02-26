"""
PlotEZ Backend Utilities.

Utility classes and functions for plot parameter management and data validation.
"""

__all__ = [
    "LinePlotConfig",
    "ScatterPlotConfig",
    "ErrorPlotConfig",
    "FigureConfig",
    "ErrorBandConfig",
    "plot_or_scatter",
    "split_dictionary",
    "dual_axes_data_validation",
    "dual_axes_label_management",
]

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, List, Literal, Tuple

from matplotlib.typing import ColorType
from numpy.typing import ArrayLike

from plotez.backend import ERROR_ATTRS, ERROR_BAND_ATTRS, LINE_ATTRS, SCATTER_ATTRS, SUBPLOT_ATTRS

label_management = Tuple[str, str, str, str, List[str]]


def _populate(_class, dictionary: dict[str, Any], mapping):
    mapped = {mapping.get(k, k): v for k, v in dictionary.items()}

    known_fields = _class.__dict__["__annotations__"].keys() - {"_extra"}

    known = {k: v for k, v in mapped.items() if k in known_fields}
    extra = {k: v for k, v in mapped.items() if k not in known_fields}

    return _class(**known, _extra=extra)


@dataclass
class LinePlotConfig:
    """Configuration class for line plots."""

    color: str | ColorType | Sequence[ColorType] | None = None
    linewidth: float | Sequence[float] | None = None
    linestyle: str | Sequence[str] | None = None
    alpha: float | Sequence[float] | None = None
    marker: str | Sequence[str] | None = None
    markersize: float | Sequence[float] | None = None
    markerfacecolor: str | Sequence[str] | None = None
    markeredgecolor: str | Sequence[str] | None = None
    markeredgewidth: float | Sequence[float] | None = None

    # For extra params - pass as dict to this field directly
    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "LinePlotConfig":
        """Create a LinePlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(_class=cls, dictionary=dictionary, mapping=LINE_ATTRS)

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Pretty repr showing both explicit and extra params."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"


@dataclass
class ErrorBandConfig:
    """Configuration class for error bands."""

    color: str | None = None
    alpha: float = 0.25
    linewidth: float | None = None
    edgecolor: str | ColorType | None = None
    linestyle: str | None = None
    hatch: str | Literal["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"] | None = None
    interpolate: bool = False
    step: str | Literal["pre", "post", "mid"] | None = None

    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ErrorBandConfig":
        """Create an ErrorBandConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(_class=cls, dictionary=dictionary, mapping=ERROR_BAND_ATTRS)

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Return a string representation of the ErrorBandConfig instance."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"


@dataclass
class ErrorPlotConfig:
    """Configuration class for error plots."""

    # Core signal identity
    color: str | None = None
    linewidth: float | None = None
    linestyle: str | None = None
    alpha: float | None = None

    # Error structure (second layer of perception)
    ecolor: str | None = None
    elinewidth: float | None = None

    # Markers (data discreteness)
    marker: str | None = None
    markersize: float | None = None
    markerfacecolor: str | None = None
    markeredgecolor: str | None = None

    # Visual refinement
    capsize: float | None = None
    capthick: float | None = None

    # For extra params - pass as dict to this field directly
    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ErrorPlotConfig":
        """Create an ErrorPlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(_class=cls, dictionary=dictionary, mapping=ERROR_ATTRS)

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Pretty repr showing both explicit and extra params."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"


@dataclass
class ScatterPlotConfig:
    """Configuration class for scatter plots."""

    c: str | None = None
    s: float | None = None
    alpha: float | None = None
    marker: str | None = None
    cmap: str | None = None
    edgecolors: str | None = None
    facecolors: str | None = None

    # For extra params - pass as dict to this field directly
    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ScatterPlotConfig":
        """Create a ScatterPlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(_class=cls, dictionary=dictionary, mapping=SCATTER_ATTRS)

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Pretty repr showing both explicit and extra params."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"


@dataclass
class FigureConfig:
    """Configuration class for subplots."""

    nrows: int = 1
    ncols: int = 1
    figsize: tuple[float, float] = (6.4, 4.8)

    sharex: bool = False
    sharey: bool = False

    constrained_layout: bool = False
    wspace: float | None = None
    hspace: float | None = None

    # For extra params - pass as dict to this field directly
    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "FigureConfig":
        """Create a FigureConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(_class=cls, dictionary=dictionary, mapping=SUBPLOT_ATTRS)

    def get_dict(self) -> dict[str, Any]:
        """Get all parameters as dict for matplotlib."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
        result.update(self._extra)
        return result

    def __repr__(self):
        """Pretty repr showing both explicit and extra params."""
        all_params = self.get_dict()
        param_str = ", ".join(f"{k}={v!r}" for k, v in sorted(all_params.items()))
        return f"{self.__class__.__name__}({param_str})"


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
    Split a `LinePlot`, `ScatterPlot`, or `ErrorPlotConfig` instance's parameters into two separate instances.

    Parameters
    ----------
    plot_instance : Union[LinePlot, ScatterPlot, ErrorPlotConfig]
        An instance of `LinePlot`, `ScatterPlot`, or `ErrorPlotConfig` with parameters stored as lists or tuples.
        Each parameter should be a list or tuple containing exactly two values, corresponding to settings for the
        two resulting instances.

    Returns
    -------
    Tuple[Union[LinePlot, ScatterPlot, ErrorPlotConfig], Union[LinePlot, ScatterPlot, ErrorPlotConfig]]
        Two instances of the same type as `plot_instance` (either `LinePlot`, `ScatterPlot`, or `ErrorPlotConfig`),
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
