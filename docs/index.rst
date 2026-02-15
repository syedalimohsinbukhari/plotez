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
* **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
* **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling
* **File Integration**: Direct plotting from CSV files
* **Extensive Customization**: Full control over plot appearance via parameter classes
* **Type Safety**: Complete type hints for better IDE support and type checking
* **Well Tested**: Comprehensive test suite with 70%+ coverage

Quick Example
-------------

.. code-block:: python

   import numpy as np
   from plotez import plot_xy

   # Generate data
   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Create plot with automatic labeling
   plot_xy(x, y, auto_label=True)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

