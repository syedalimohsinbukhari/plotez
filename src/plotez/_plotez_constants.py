"""Created on Jan 07 14:42:35 2026.

Copied over and modified from GRBResearch repository
"""

__all__ = [
    # Font sizes
    "LABEL_FONT_SIZE",
    "LEGEND_TITLE_FONT_SIZE",
    "LEGEND_FONT_SIZE",
    "TICK_FONT_SIZE",
    "TITLE_FONT_SIZE",
    "ANNOTATION_FONT_SIZE",
    # Figure / line / marker geometry
    "FIGURE_DPI",
    "SAVE_DPI",
    "DEFAULT_FIGURE_SIZE",
    "LINE_WIDTH",
    "MARKER_SIZE",
    "CAP_SIZE",
    "AXES_LINE_WIDTH",
    # Tick geometry
    "TICK_MAJOR_SIZE",
    "TICK_MAJOR_WIDTH",
    "TICK_MINOR_SIZE",
    "TICK_MINOR_WIDTH",
    "TICK_DIRECTION",
    # Grid
    "GRID_ALPHA",
    "GRID_LINESTYLE",
    "update_style",
    "enable_style",
    "disable_style",
]

from matplotlib import pyplot as plt

LABEL_FONT_SIZE = 12
LEGEND_FONT_SIZE = 10
LEGEND_TITLE_FONT_SIZE = LEGEND_FONT_SIZE
TICK_FONT_SIZE = 12
TITLE_FONT_SIZE = 13
ANNOTATION_FONT_SIZE = 10

# Figure / line / marker geometry
FIGURE_DPI = 150
SAVE_DPI = 600
DEFAULT_FIGURE_SIZE = (8, 6)
LINE_WIDTH = 1.0
MARKER_SIZE = 6
CAP_SIZE = 5
AXES_LINE_WIDTH = 0.8

# Tick geometry
TICK_MAJOR_SIZE = 5
TICK_MAJOR_WIDTH = 0.8
TICK_MINOR_SIZE = 3
TICK_MINOR_WIDTH = 0.6
TICK_DIRECTION = "in"  # astronomy convention

# Grid
GRID_ALPHA = 0.25
GRID_LINESTYLE = "--"


def update_style(grid: bool = True):
    """Update style for publication-ready figures.

    All values are driven by constants in grb_constants — a single source of truth.
    Changing a constant there automatically updates every figure.

    Parameters
    ----------
    grid :
        Whether `axes.grid` should be enabled by plotez's convention. Default is `True`.
        Set to `False` to keep every other styling choice but leave grids off.
    """
    plt.rcParams.update(
        {
            # Font
            "font.family": "serif",
            "mathtext.fontset": "cm",
            "font.size": LABEL_FONT_SIZE,
            "axes.labelsize": LABEL_FONT_SIZE,
            "axes.titlesize": TITLE_FONT_SIZE,
            "xtick.labelsize": TICK_FONT_SIZE,
            "ytick.labelsize": TICK_FONT_SIZE,
            "legend.fontsize": LEGEND_FONT_SIZE,
            "legend.title_fontsize": LEGEND_TITLE_FONT_SIZE,
            # Figure
            "figure.dpi": FIGURE_DPI,
            "figure.figsize": DEFAULT_FIGURE_SIZE,
            "savefig.dpi": SAVE_DPI,
            "savefig.bbox": "tight",
            # Lines / markers
            "lines.linewidth": LINE_WIDTH,
            "lines.markersize": MARKER_SIZE,
            "axes.linewidth": AXES_LINE_WIDTH,
            # 'scatter.size': MARKER_SIZE,
            # Ticks
            "xtick.major.size": TICK_MAJOR_SIZE,
            "xtick.major.width": TICK_MAJOR_WIDTH,
            "xtick.minor.size": TICK_MINOR_SIZE,
            "xtick.minor.width": TICK_MINOR_WIDTH,
            "xtick.minor.visible": True,
            "xtick.direction": TICK_DIRECTION,
            "ytick.major.size": TICK_MAJOR_SIZE,
            "ytick.major.width": TICK_MAJOR_WIDTH,
            "ytick.minor.size": TICK_MINOR_SIZE,
            "ytick.minor.width": TICK_MINOR_WIDTH,
            "ytick.minor.visible": True,
            "ytick.direction": TICK_DIRECTION,
            # Grid
            "axes.grid": grid,
            "grid.alpha": GRID_ALPHA,
            "grid.linestyle": GRID_LINESTYLE,
            "axes.axisbelow": True,
        }
    )


def enable_style(grid: bool = True):
    """(Re-)apply plotez's publication-ready rcParams convention.

    Alias for :func:`update_style`, kept as the counterpart to :func:`disable_style` so users can toggle
    plotez's styling on and off at will.

    Parameters
    ----------
    grid :
        Whether `axes.grid` should be enabled. Default is `True`.
    """
    update_style(grid=grid)


def disable_style():
    """Turn off plotez's styling convention, restoring matplotlib's own defaults.

    Use this if you'd rather manage rcParams yourself after plotez has applied its convention on import.
    """
    plt.rcdefaults()
