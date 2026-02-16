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
* **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
* **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling
* **File Integration**: Direct plotting from CSV files
* **Extensive Customization**: Full control over plot appearance via parameter classes
* **Inheritance-Based Design**: ErrorPlot inherits from LinePlot for consistent styling
* **Type Safety**: Complete type hints for better IDE support and type checking
* **Well Tested**: Comprehensive test suite with 70%+ coverage

Quick Example
-------------

.. code-block:: python

   import numpy as np
   from plotez import plot_xy, plot_errorbars
   from plotez.backend.utilities import ErrorPlot

   # Basic line plot
   x = np.linspace(0, 10, 100)
   y = np.sin(x)
   plot_xy(x, y, auto_label=True)

   # Error bar plot with enhanced styling
   x_sparse = np.linspace(0, 10, 20)
   y_sparse = np.sin(x_sparse)
   y_err = 0.1 * np.random.rand(len(y_sparse))

   ep = ErrorPlot(
       line_style='-',
       color='blue',
       marker='o',
       capsize=5,
       ecolor='red'  # Different color for error bars
   )
   plot_errorbars(x_sparse, y_sparse, y_err=y_err, plot_dictionary=ep)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

