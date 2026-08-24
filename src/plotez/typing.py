"""Type aliases used throughout PlotEZ.

.. list-table:: Public aliases
   :header-rows: 1
   :widths: 10 90

   * - Name
     - Description
   * - ``NDArray``
     - Re-export of :class:`numpy.ndarray` but as a typehint – any array-like input accepted by NumPy.
   * - ``AxesReturn``
     - ``Axes | tuple[Axes, Axes]`` – return type for single- and dual-axis plot functions.
       Grid functions (``n_plotter``, ``two_subplots``) return a shaped ``NDArray`` of
       ``Axes`` directly.
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

HatchStyle = Literal["/", "\\", "///", "|", "-", "+", "x", "o", "O", ".", "*"]

AxesReturn = Axes | tuple[Axes, Axes]

if TYPE_CHECKING:
    from . import ErrorBandConfig, ErrorPlotConfig, LinePlotConfig, ScatterPlotConfig

    LSE = LinePlotConfig | ScatterPlotConfig | ErrorPlotConfig | ErrorBandConfig
