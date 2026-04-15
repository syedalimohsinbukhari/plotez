"""Type aliases used throughout PlotEZ.

.. list-table:: Public aliases
   :header-rows: 1
   :widths: 10 90

   * - Name
     - Description
   * - ``ArrayLike``
     - Re-export of :class:`numpy.typing.ArrayLike` – any array-like input accepted by NumPy.
   * - ``AxesReturn``
     - ``Axes | tuple[Axes, Axes]`` – return type for single- or dual-axis plot functions.
   * - ``AxesFigReturn``
     - ``Axes | tuple[Figure, Axes]`` – return type for functions that may create a new figure.
   * - ``LABEL_MGMT``
     - ``tuple[str, str, str, str, list[str]]`` – internal label bundle returned by
       :func:`~plotez.backend.utilities.dual_axes_label_management`.
   * - ``LSE``
     - Union of all four config classes (type-checking only):
       ``LinePlotConfig | ScatterPlotConfig | ErrorPlotConfig | ErrorBandConfig``.
"""

from typing import TYPE_CHECKING

from matplotlib.axes import Axes as _Axes
from matplotlib.figure import Figure as _Figure
from numpy.typing import ArrayLike as _ArrayLike

ArrayLike = _ArrayLike

AxesReturn = _Axes | tuple[_Axes, _Axes]
AxesFigReturn = _Axes | tuple[_Figure, _Axes]

LABEL_MGMT = tuple[str, str, str, str, list[str]]

if TYPE_CHECKING:
    from . import ErrorBandConfig, ErrorPlotConfig, LinePlotConfig, ScatterPlotConfig

    LSE = LinePlotConfig | ScatterPlotConfig | ErrorPlotConfig | ErrorBandConfig
