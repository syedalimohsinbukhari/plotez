"""Type aliases used throughout PlotEZ.

.. list-table:: Public aliases
   :header-rows: 1
   :widths: 10 90

   * - Name
     - Description
   * - ``NDArray``
     - Re-export of :class:`numpy.ndarray` but as a typehint – any array-like input accepted by NumPy.
   * - ``AxesReturn``
     - ``Axes | tuple[Axes, Axes] | NDArray`` – unified return type for all plot functions.
       Single-axis functions return ``Axes``; dual-axis functions return ``tuple[Axes, Axes]``;
       grid functions (``n_plotter``, ``two_subplots``) return a shaped ``NDArray`` of ``Axes``.
"""

from typing import TYPE_CHECKING, Literal

import numpy as np
from matplotlib.axes import Axes as _Axes
from matplotlib.figure import Figure as _Figure
from numpy.typing import ArrayLike as _ArrayLike

NDArray = np.ndarray
ArrayLike = _ArrayLike
Axes = _Axes
Figure = _Figure

HatchStyle = Literal["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]

AxesReturn = Axes | tuple[Axes, Axes]

# Deprecated – kept as a backward-compatible alias; will be removed in a future release.
AxesFigReturn = AxesReturn

# LABEL_MGMT = tuple[str, str, str, str, list[str | None]]

if TYPE_CHECKING:
    from . import ErrorBandConfig, ErrorPlotConfig, LinePlotConfig, ScatterPlotConfig

    LSE = LinePlotConfig | ScatterPlotConfig | ErrorPlotConfig | ErrorBandConfig
