"""
PlotEZ Backend Utilities.

Utility classes and functions for plot parameter management and data validation.
"""

from __future__ import annotations

__all__ = [
    "LinePlotConfig",
    "ScatterPlotConfig",
    "ErrorPlotConfig",
    "ErrorBandConfig",
    "plot_or_scatter",
    "split_dictionary",
    "dual_axes_data_validation",
    "dual_axes_label_management",
]

from dataclasses import dataclass, field
from typing import Any, Literal, Sequence
from warnings import warn

from numpy.typing import ArrayLike

from plotez.backend.CONSTANTS import ERROR_ATTRS, ERROR_BAND_ATTRS, LINE_ATTRS, SCATTER_ATTRS
from plotez.backend.error_handling import (
    AxisLabelError,
    EmptyDataError,
    LabelConflictWarning,
    TwinXDataError,
    TwinYDataError,
)

label_management = tuple[str, str, str, str, list[str]]


def _populate(_class, dictionary: dict[str, Any], mapping):
    """
    Create a config dataclass instance from a dictionary, applying key aliases.

    Parameters
    ----------
    _class :
        The dataclass type to instantiate.
    dictionary :
        Raw parameter dictionary, possibly using shorthand keys.
    mapping :
        Alias-to-canonical-name mapping for shorthand keys.

    Returns
    -------
    instance
        An instance of ``_class`` populated from the mapped dictionary.
    """
    mapped = {mapping.get(k, k): v for k, v in dictionary.items()}

    known_fields = _class.__dict__["__annotations__"].keys() - {"_extra"}

    known = {k: v for k, v in mapped.items() if k in known_fields}
    extra = {k: v for k, v in mapped.items() if k not in known_fields}

    return _class(**known, _extra=extra)


@dataclass
class LinePlotConfig:
    """Configuration class for line plots."""

    color: str | Sequence[str] | None = None
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
    """Configuration class for error bands (shaded fill regions)."""

    color: str | None = None
    alpha: float = 0.25
    linewidth: float | None = None
    edgecolor: str | None = None
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
    """Configuration class for error bar plots."""

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
    errorevery: int | tuple | None = None

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


LSE = LinePlotConfig | ScatterPlotConfig | ErrorPlotConfig | ErrorBandConfig


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


def split_dictionary(plot_instance: LSE) -> tuple[LSE, LSE]:
    """
    Split a config instance's parameters into two separate instances.

    Parameters
    ----------
    plot_instance :
        An instance with parameters stored as lists or tuples.
        Each parameter should be a list or tuple containing exactly two values, corresponding to settings for the
        two resulting instances.

    Returns
    -------
    Tuple
        Two instances of the same type as `plot_instance`, with parameters split based on the values in `plot_instance`.
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
    AxisLabelError
        If ``axis_labels`` does not have exactly three elements.
    EmptyDataError
        If ``x1_data`` or ``y1_data`` is empty.
    TwinXDataError
        If ``x2_data`` is provided when ``use_twin_x`` is ``True``.
    TwinYDataError
        If ``y2_data`` is provided when ``use_twin_x`` is ``False``.
    """
    if len(axis_labels) != 3:
        raise AxisLabelError("The axis_labels should have a length of 3.")
    if len(x1_data) == 0 or len(y1_data) == 0:
        raise EmptyDataError("Primary x or y data is empty. Please provide valid data.")
    if use_twin_x and x2_data is not None:
        raise TwinXDataError("Dual Y-axis plot requested but 'x2_data' given.")
    if not use_twin_x and y2_data is not None:
        raise TwinYDataError("Dual X-axis plot requested but 'y2_data' given.")


def dual_axes_label_management(
    x1y1_label: str | None = None,
    x1y2_label: str | None = None,
    x2y1_label: str | None = None,
    auto_label: bool = False,
    axis_labels: Sequence[str] | None = None,
    plot_title: str | None = None,
    use_twin_x: bool = True,
) -> label_management:
    """
    Manage labels and titles for dual-axes plots.

    Parameters
    ----------
    x1y1_label : str, optional
        Label for the primary plot (X1 vs. Y1).
        Ignored if `auto_label=True`.
    x1y2_label : str, optional
        Label for the secondary Y-axis plot (X1 vs. Y2), used if `use_twin_x` is True.
        Ignored if `auto_label=True`.
    x2y1_label : str, optional
        Label for the secondary X-axis plot (X2 vs. Y1), used if `use_twin_x` is False.
        Ignored if `auto_label=True`.
    auto_label : bool, default False
        If True, **overwrites all provided labels** with automatic defaults.
        When True, all label parameters are ignored.
    axis_labels : Sequence[str], optional
        Axis labels as [x_label, y1_label, y2_or_x2_label].
        Ignored if `auto_label=True`.
        - Dual Y-axis: [primary x, primary y, secondary y]
        - Dual X-axis: [primary x, primary y, secondary x]
    plot_title : str, optional
        Plot title. Ignored if `auto_label=True`.
    use_twin_x : bool, default True
        If True, dual Y-axis plot. If False, dual X-axis plot.

    Returns
    -------
    tuple[str, str, str, str, list[str]]
        (x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels)

    Notes
    -----
    When `auto_label=True`, all user-provided labels are **replaced** with:
      - Dual Y-axis defaults: axis_labels=['X', 'Y₁', 'Y₂'], x1y1_label='X₁ vs. Y₁', x1y2_label='X₁ vs. Y₂'
      - Dual X-axis defaults: axis_labels=['X₁', 'Y', 'X₂'], x1y1_label='Y vs. X₁', x2y1_label='Y vs. X₂'
      - plot_title='Plot'

    When `auto_label=False`, missing labels are replaced with empty strings.
    """
    # Warn if the user provided labels but `auto_label` is True
    if auto_label:
        _auto_handler(axis_labels=axis_labels, x1y1_label=x1y1_label, x1y2_label=x1y2_label, x2y1_label=x2y1_label)
    if auto_label:
        # Auto-label OVERWRITES everything
        if use_twin_x:
            axis_labels = ["X", r"$Y_1$", r"$Y_2$"]
            x1y1_label = r"$X_1$ vs $Y_1$"
            x1y2_label = r"$X_1$ vs $Y_2$"
            x2y1_label = ""
        else:
            axis_labels = [r"$X_1$", "Y", r"$X_2$"]
            x1y1_label = r"Y vs $X_1$"
            x1y2_label = ""
            x2y1_label = r"Y vs $X_2$"
        plot_title = "Plot"
    else:
        # Use provided values or empty strings
        axis_labels = list(axis_labels) if axis_labels else ["", "", ""]
        x1y1_label = x1y1_label or ""
        x1y2_label = x1y2_label or ""
        x2y1_label = x2y1_label or ""
        plot_title = plot_title or ""

    return x1y1_label, x1y2_label, x2y1_label, plot_title, axis_labels


def _auto_handler(
    axis_labels: Sequence[str] | None, x1y1_label: str | None, x1y2_label: str | None, x2y1_label: str | None
):
    provided_labels = []
    if x1y1_label is not None:
        provided_labels.append("x1y1_label")
    if x1y2_label is not None:
        provided_labels.append("x1y2_label")
    if x2y1_label is not None:
        provided_labels.append("x2y1_label")
    if axis_labels is not None and not all(x is None for x in axis_labels):
        provided_labels.append("axis_labels")

    if provided_labels:
        warn(
            message=f"`auto_label=True` will override provided labels: {', '.join(provided_labels)}",
            category=LabelConflictWarning,
            stacklevel=2,
        )
