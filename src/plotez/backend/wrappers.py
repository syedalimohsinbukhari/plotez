"""Created on Mar 07 20:32:48 2026."""

from typing import Literal

from plotez.typing import HatchStyle

from ..configurations import ErrorBandConfig, ErrorPlotConfig, HistogramConfig, LinePlotConfig, ScatterPlotConfig

__all__ = [
    "ebc",
    "epc",
    "error_band_configuration",
    "error_plot_configuration",
    "hgc",
    "histogram_config",
    "line_plot_configuration",
    "lpc",
    "scatter_plot_configuration",
    "spc",
]


def line_plot_configuration(
    c: str | list[str] | None = None,
    lw: float | list[float] | None = None,
    ls: str | list[str] | None = None,
    alpha: float | list[float] | None = None,
    marker: str | list[str] | None = None,
    ms: float | list[float] | None = None,
    mfc: str | list[str] | None = None,
    mec: str | list[str] | None = None,
    mew: float | list[float] | None = None,
    **kwargs,
):
    """
    Create a configuration object for line plots.

    Parameters
    ----------
    c :
        Line color.
    lw :
        Line width.
    ls :
        Line style (e.g., '-', '--', '-.', ':').
    alpha :
        Transparency level (0.0 to 1.0).
    marker :
        Marker style (e.g., 'o', 's', '^').
    ms :
        Marker size.
    mfc :
        Marker face color.
    mec :
        Marker edge color.
    mew :
        Marker-edge width.
    **kwargs :
        Additional keyword arguments passed to the underlying plot function.

    Returns
    -------
    LinePlotConfig
        Configuration object for line plots.
    """
    return LinePlotConfig(
        color=c,
        linewidth=lw,
        linestyle=ls,
        alpha=alpha,
        marker=marker,
        markersize=ms,
        markeredgecolor=mec,
        markerfacecolor=mfc,
        markeredgewidth=mew,
        _extra=kwargs,
    )


def error_band_configuration(
    c: str | None = None,
    alpha: float = 0.25,
    lw: float | None = None,
    ec: str | None = None,
    ls: str | None = None,
    hatch: HatchStyle | list[HatchStyle] | None = None,
    interpolate: bool | None = None,
    step: str | Literal["pre", "post", "mid"] | None = None,
    **kwargs,
):
    """
    Create a configuration object for error bands.

    Parameters
    ----------
    c :
        Fill color for the error band.
    alpha :
        Transparency level (0.0 to 1.0).
    lw :
        Edge line width.
    ec :
        Edge color.
    ls :
        Edge line style (e.g., '-', '--', '-.', ':').
    hatch :
        Hatching pattern (e.g., '/', '|', '-', '+', 'x').
    interpolate :
        Whether to interpolate the error band.
    step :
        Step mode for the band (e.g., 'pre', 'post', 'mid').
    **kwargs :
        Additional keyword arguments passed to the underlying fill function.

    Returns
    -------
    ErrorBandConfig
        Configuration object for error bands.
    """
    return ErrorBandConfig(
        color=c,
        alpha=alpha,
        linewidth=lw,
        edgecolor=ec,
        linestyle=ls,
        hatch=hatch,
        interpolate=interpolate,
        step=step,
        _extra=kwargs,
    )


def error_plot_configuration(
    c: str | None = None,
    lw: float | None = None,
    ls: str | None = None,
    alpha: float | None = None,
    ecolor: str | None = None,
    elinewidth: float | None = None,
    marker: str | None = None,
    ms: float | None = None,
    mfc: str | None = None,
    mec: str | None = None,
    capsize: float | None = None,
    capthick: float | None = None,
    errorevery: int | tuple | None = None,
    **kwargs,
):
    """
    Create a configuration object for error bar plots.

    Parameters
    ----------
    c :
        Line color.
    lw :
        Line width.
    ls :
        Line style (e.g., '-', '--', '-.', ':').
    alpha :
        Transparency level (0.0 to 1.0).
    ecolor :
        Error bar color.
    elinewidth :
        Error bar line width.
    marker :
        Marker style (e.g., 'o', 's', '^').
    ms :
        Marker size.
    mfc :
        Marker face color.
    mec :
        Marker edge color.
    capsize :
        Length of the error bar caps in points.
    capthick :
        Thickness of error bar caps.
    errorevery :
        Draw error bars on a subset of data points.
    **kwargs :
        Additional keyword arguments passed to the underlying errorbar function.

    Returns
    -------
    ErrorPlotConfig
        Configuration object for error bar plots.
    """
    return ErrorPlotConfig(
        color=c,
        linewidth=lw,
        linestyle=ls,
        alpha=alpha,
        ecolor=ecolor,
        elinewidth=elinewidth,
        marker=marker,
        markersize=ms,
        markeredgecolor=mec,
        markerfacecolor=mfc,
        capsize=capsize,
        capthick=capthick,
        errorevery=errorevery,
        _extra=kwargs,
    )


def scatter_plot_configuration(
    c: str | list[str] | None = None,
    s: float | list[float] | None = None,
    alpha: float | list[float] | None = None,
    marker: str | list[str] | None = None,
    cmap: str | list[str] | None = None,
    ec: str | list[str] | None = None,
    fc: str | list[str] | None = None,
    **kwargs,
):
    """
    Create a configuration object for scatter plots.

    Parameters
    ----------
    c :
        Marker color(s).
    s :
        Marker size(s) in points squared.
    alpha :
        Transparency level (0.0 to 1.0).
    marker :
        Marker style (e.g., 'o', 's', '^').
    cmap :
        Colormap name or object.
    ec :
        Edge color(s).
    fc :
        Face color(s).
    **kwargs :
        Additional keyword arguments passed to the underlying scatter function.

    Returns
    -------
    ScatterPlotConfig
        Configuration object for scatter plots.
    """
    return ScatterPlotConfig(
        color=c, s=s, alpha=alpha, marker=marker, cmap=cmap, edgecolors=ec, facecolors=fc, _extra=kwargs
    )


def histogram_config(
    bins: int | None = None,
    density: bool | None = None,
    histtype: str | None = None,
    color: str | None = None,
    alpha: float | None = None,
    edgecolor: str | None = None,
    facecolor: str | None = None,
    linewidth: float | None = None,
    orientation: str | None = None,
    cumulative: bool | None = None,
    hatch: HatchStyle | None = None,
    **kwargs,
):
    """
    Create a configuration object for histogram plots.

    Parameters
    ----------
    bins :
        Number of histogram bins.
    density :
        If `True`, normalize the histogram to form a probability density.
    histtype :
        Histogram drawing style (e.g., 'bar', 'barstacked', 'step', 'stepfilled').
    color :
        Bar color.
    alpha :
        Transparency level (0.0 to 1.0).
    edgecolor :
        Edge color of the bars.
    facecolor :
        Face color of the bars.
    linewidth :
        Edge line width.
    orientation :
        Orientation of the histogram (e.g., 'vertical', 'horizontal').
    cumulative :
        If `True`, each bin gives the counts in that bin plus all bins for smaller values.
    hatch :
        Hatching pattern (e.g., '/', '|', '-', '+', 'x').
    **kwargs :
        Additional keyword arguments passed to the underlying histogram function.

    Returns
    -------
    HistogramConfig
        Configuration object for histogram plots.
    """
    return HistogramConfig(
        bins=bins,
        density=density,
        histtype=histtype,
        color=color,
        alpha=alpha,
        edgecolor=edgecolor,
        facecolor=facecolor,
        linewidth=linewidth,
        orientation=orientation,
        cumulative=cumulative,
        hatch=hatch,
        _extra=kwargs,
    )


lpc = line_plot_configuration
epc = error_plot_configuration
ebc = error_band_configuration
spc = scatter_plot_configuration
hgc = histogram_config
