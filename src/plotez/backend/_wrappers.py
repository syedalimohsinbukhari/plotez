"""Created on Mar 07 20:32:48 2026."""

from collections.abc import Sequence
from typing import Literal

from .utilities import ErrorBandConfig, ErrorPlotConfig, LinePlotConfig, ScatterPlotConfig

__all__ = [
    "line_plot_configuration",
    "scatter_plot_configuration",
    "error_plot_configuration",
    "error_band_configuration",
    "lpc",
    "spc",
    "epc",
    "ebc",
]


def line_plot_configuration(
    c: str | Sequence[str] | None = None,
    lw: float | Sequence[float] | None = None,
    ls: str | Sequence[str] | None = None,
    alpha: float | Sequence[float] | None = None,
    marker: str | Sequence[str] | None = None,
    ms: float | Sequence[float] | None = None,
    mfc: str | Sequence[str] | None = None,
    mec: str | Sequence[str] | None = None,
    mew: float | Sequence[float] | None = None,
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
        Marker edge width.
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
    hatch: str | Literal["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"] | None = None,
    interpolate: bool = False,
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
    c: str | None = None,
    s: float | None = None,
    alpha: float | None = None,
    marker: str | None = None,
    cmap: str | None = None,
    ec: str | None = None,
    fc: str | None = None,
    **kwargs,
):
    """
    Create a configuration object for scatter plots.

    Parameters
    ----------
    c : color or array-like, optional
        Marker color(s).
    s : float or array-like, optional
        Marker size(s) in points squared.
    alpha : float, optional
        Transparency level (0.0 to 1.0).
    marker : str, optional
        Marker style (e.g., 'o', 's', '^').
    cmap : str or Colormap, optional
        Colormap name or object.
    ec : color or array-like, optional
        Edge color(s).
    fc : color or array-like, optional
        Face color(s).
    **kwargs : dict, optional
        Additional keyword arguments passed to the underlying scatter function.

    Returns
    -------
    ScatterPlotConfig
        Configuration object for scatter plots.
    """
    return ScatterPlotConfig(
        c=c, s=s, alpha=alpha, marker=marker, cmap=cmap, edgecolors=ec, facecolors=fc, _extra=kwargs
    )


lpc = line_plot_configuration
epc = error_plot_configuration
ebc = error_band_configuration
spc = scatter_plot_configuration
