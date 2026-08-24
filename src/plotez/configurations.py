"""Created on Jun 16 10:15:07 2026."""

from dataclasses import dataclass
from typing import Any, Literal

from .backend.base_config import PlotEZConfig
from .backend.CONSTANTS import BAR_PLOT_ATTRS, ERROR_ATTRS, ERROR_BAND_ATTRS, HIST_ATTRS, LINE_ATTRS, SCATTER_ATTRS
from .typing import HatchStyle


def _populate(cls_, dictionary: dict[str, Any], mapping):
    """
    Create a config dataclass instance from a dictionary, applying key aliases.

    Parameters
    ----------
    cls_ :
        The dataclass type to instantiate.
    dictionary :
        Raw parameter dictionary, possibly using shorthand keys.
    mapping :
        Alias-to-canonical-name mapping for shorthand keys.

    Returns
    -------
    instance :
        An instance of ``_class`` populated from the mapped dictionary.
    """
    mapped = {mapping.get(k, k): v for k, v in dictionary.items()}

    known_fields = cls_.__dict__["__annotations__"].keys() - {"_extra"}

    known = {k: v for k, v in mapped.items() if k in known_fields}
    extra = {k: v for k, v in mapped.items() if k not in known_fields}

    return cls_(**known, _extra=extra)


@dataclass(repr=False)
class ScatterPlotConfig(PlotEZConfig):
    """Configuration class for scatter plots."""

    color: str | list[str] | None = None
    s: float | list[float] | None = None
    alpha: float | list[float] | None = None
    marker: str | list[str] | None = None
    cmap: str | list[str] | None = None
    edgecolors: str | list[str] | None = None
    facecolors: str | list[str] | None = None

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ScatterPlotConfig":
        """Create a ScatterPlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=SCATTER_ATTRS)


@dataclass(repr=False)
class ErrorBandConfig(PlotEZConfig):
    """Configuration class for error bands (shaded fill regions)."""

    color: str | list[str] | None = None
    alpha: float | list[float] = 0.25
    linewidth: float | list[float] | None = None
    edgecolor: str | list[str] | None = None
    linestyle: str | list[str] | None = None
    hatch: HatchStyle | list[HatchStyle] | None = None
    interpolate: bool | None = None
    step: str | Literal["pre", "post", "mid"] | None = None

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ErrorBandConfig":
        """Create an ErrorBandConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=ERROR_BAND_ATTRS)


@dataclass(repr=False)
class ErrorPlotConfig(PlotEZConfig):
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

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "ErrorPlotConfig":
        """Create an ErrorPlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=ERROR_ATTRS)


@dataclass(repr=False)
class HistogramConfig(PlotEZConfig):
    """Configuration class for histogram plots."""

    bins: int | None = None
    density: bool | None = None
    histtype: str | None = None
    color: str | None = None
    alpha: float | None = None
    edgecolor: str | None = None
    facecolor: str | None = None
    linewidth: float | None = None
    orientation: str | None = None
    cumulative: bool | None = None
    hatch: HatchStyle | None = None

    @classmethod
    def populate(cls, dictionary: dict[str, Any]):
        """Create a HistogramConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=HIST_ATTRS)


@dataclass(repr=False)
class LinePlotConfig(PlotEZConfig):
    """Configuration class for line plots."""

    color: str | list[str] | None = None
    linewidth: float | list[float] | None = None
    linestyle: str | list[str] | None = None
    alpha: float | list[float] | None = None
    marker: str | list[str] | None = None
    markersize: float | list[float] | None = None
    markerfacecolor: str | list[str] | None = None
    markeredgecolor: str | list[str] | None = None
    markeredgewidth: float | list[float] | None = None

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "LinePlotConfig":
        """Create a LinePlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=LINE_ATTRS)


@dataclass(repr=False)
class BarPlotConfig(PlotEZConfig):
    """Configuration class for bar/hbar plots."""

    color: str | list[str] | None = None
    edgecolor: str | list[str] | None = None
    linewidth: float | list[float] | None = None
    alpha: float | list[float] | None = None
    width: float | list[float] | None = None  # bar width for plot_bar; routed to height for plot_hbar
    align: str | None = None  # 'center' or 'edge'
    capsize: float | None = None  # error bar cap size; first-class since errors= is first-class
    ecolor: str | None = None  # error bar color
    hatch: HatchStyle | list[HatchStyle] | None = None

    @classmethod
    def populate(cls, dictionary: dict[str, Any]) -> "BarPlotConfig":
        """Create a ScatterPlotConfig instance from a dictionary, using a mapping for shorthand keys."""
        return _populate(cls_=cls, dictionary=dictionary, mapping=BAR_PLOT_ATTRS)
