PlotEZ Documentation
====================

**PlotEZ** - Mundane plotting made easy.

PlotEZ is a Python library that simplifies common matplotlib plotting tasks with an intuitive API.
It provides convenient functions for creating single plots, dual-axis plots, and multi-panel figures
with minimal boilerplate code.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   CHANGELOG

Features
--------

* **Simple API**: Create complex plots with just a few lines of code
* **Error Bar Plotting**: Comprehensive error bar support with enhanced styling options
* **Error Band Plotting**: Shaded error band support via ``plot_errorband``, ``plot_errorband_relative``, and ``ErrorBandConfig``
* **Histogram & Density Plotting**: ``plot_hist`` and ``plot_density`` with ``HistogramConfig`` / ``hgc``
* **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
* **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling; layout (``tight_layout``) is fully user-controlled
* **File Integration**: Direct plotting from CSV files
* **Axes-Only Returns**: All functions return ``Axes`` (or shaped ``ndarray`` of ``Axes`` for grid functions); the parent ``Figure`` is always accessible via ``ax.get_figure()``
* **Extensive Customization**: Full control over plot appearance via independent config dataclasses
* **Convenience Wrappers**: Short-form factory functions (``lpc``, ``epc``, ``ebc``, ``spc``, ``hgc``) available at top level
* **Custom Exceptions**: Domain-specific exceptions for clear, catchable error handling
* **Early Input Validation**: 1D shape, matching-length, error-array, grid-size, and file-data checks fail before matplotlib
* **Type Safety**: Complete type hints for better IDE support and type checking (PEP 561 compliant)
* **Well Tested**: Comprehensive test suite with 85%+ coverage

Quick Example
-------------

.. code-block:: python

   import numpy as np
   from plotez import plot_xy, plot_errorbar, epc

   # Basic line plot
   x = np.linspace(0, 10, 100)
   y = np.sin(x)
   plot_xy(x, y, x_label="X", y_label="Y", data_label=r"$\sin(x)$")

   # Error bar plot with enhanced styling using the epc() convenience wrapper
   x_sparse = np.linspace(0, 10, 20)
   y_sparse = np.sin(x_sparse)
   y_err = 0.1 * np.random.rand(len(y_sparse))

   ep = epc(
       ls='-',
       c='blue',
       marker='o',
       capsize=5,
       ecolor='red',   # different colour for error bars
       elinewidth=1.5,
   )
   plot_errorbar(x_sparse, y_sparse, y_err=y_err, errorbar_config=ep)
