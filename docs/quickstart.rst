Quick Start Guide
=================

This guide introduces the basic usage of PlotEZ with practical examples.

Basic Plotting
--------------

Simple X vs Y Plot
~~~~~~~~~~~~~~~~~~

The simplest way to create a plot:

.. code-block:: python

   import numpy as np
   from plotez import plot_xy

   # Generate data
   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Create plot
   plot_xy(x, y, auto_label=True)

With Custom Labels
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_xy(
       x, y,
       x_label='Time (s)',
       y_label='Amplitude',
       plot_title='Sine Wave',
       data_label='sin(x)'
   )

Dual-Axis Plots
---------------

Dual Y-Axis
~~~~~~~~~~~

Plot two datasets with different y-scales:

.. code-block:: python

   from plotez import plot_xyy

   x = np.linspace(0, 10, 100)
   y1 = np.sin(x)
   y2 = np.exp(x / 10)

   plot_xyy(
       x, y1, y2,
       x_label='Time',
       y1_label='Sine',
       y2_label='Exponential',
       data_labels=['sin(x)', 'exp(x/10)'],
       plot_title='Dual Y-Axis Example'
   )

Dual X-Axis
~~~~~~~~~~~

Use ``plot_with_dual_axes`` directly for dual x-axis plots:

.. code-block:: python

   from plotez import plot_with_dual_axes

   x1 = np.linspace(0, 10, 100)
   x2 = np.linspace(0, 20, 100)
   y = np.sin(x1)

   plot_with_dual_axes(
       x1, y,
       x2_data=x2,
       use_twin_x=False,
       auto_label=True
   )

Multi-Panel Plots
-----------------

Two Subplots
~~~~~~~~~~~~

Create horizontal or vertical subplot arrangements:

.. code-block:: python

   from plotez import two_subplots

   x1 = np.linspace(0, 10, 100)
   x2 = np.linspace(0, 5, 50)
   y1 = np.sin(x1)
   y2 = np.cos(x2)

   # Horizontal layout
   fig, axs = two_subplots(
       [x1, x2], [y1, y2],
       orientation='h',
       auto_label=True
   )

   # Vertical layout
   fig, axs = two_subplots(
       [x1, x2], [y1, y2],
       orientation='v',
       plot_title='Two Subplots Example'
   )

N×M Grid
~~~~~~~~

Create arbitrary grid layouts:

.. code-block:: python

   from plotez import n_plotter

   # Create 2×2 grid
   x_data = [np.linspace(0, 10, 100) for _ in range(4)]
   y_data = [
       np.sin(x_data[0]),
       np.cos(x_data[1]),
       np.tan(x_data[2] / 5),
       x_data[3]**2 / 100
   ]

   fig, axs = n_plotter(
       x_data, y_data,
       n_rows=2, n_cols=2,
       auto_label=True
   )

Scatter Plots
-------------

Any plot function can create scatter plots:

.. code-block:: python

   from plotez import plot_xy

   x = np.random.randn(100)
   y = np.random.randn(100)

   plot_xy(x, y, is_scatter=True, auto_label=True)

Customization with Parameter Classes
-------------------------------------

Line Plots
~~~~~~~~~~

.. code-block:: python

   from plotez import plot_xy
   from plotez.backend.utilities import LinePlotConfig

   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Create custom line plot parameters
   line_params = LinePlotConfig(
       linestyle='-',
       linewidth=2,
       color='#FF5733',
       marker='o',
       markersize=4
   )

   plot_xy(x, y, plot_config=line_params)

Scatter Plots
~~~~~~~~~~~~~

.. code-block:: python

   from plotez.backend.utilities import ScatterPlotConfig

   scatter_params = ScatterPlotConfig(
       c='blue',
       s=50,
       marker='s',
       alpha=0.6
   )

   plot_xy(x, y, is_scatter=True, plot_config=scatter_params)

Subplot Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from plotez.backend.utilities import FigureConfig

   subplot_params = FigureConfig(
       sharex=True,
       sharey=True,
       figsize=(12, 8)
   )

   fig, axs = two_subplots(
       [x, x], [y, y*2],
       orientation='h',
       figure_config=subplot_params
   )

Plotting from Files
-------------------

PlotEZ can directly plot two-column CSV files:

.. code-block:: python

   from plotez import plot_two_column_file

   # Basic usage
   plot_two_column_file('data.csv')

   # With options
   plot_two_column_file(
       'data.csv',
       delimiter=',',
       skip_header=True,
       x_label='X Values',
       y_label='Y Values',
       plot_title='Data from CSV'
   )

Error Bar Plots
---------------

PlotEZ provides comprehensive error bar plotting capabilities through the ``ErrorPlotConfig`` class
and the ``plot_errorbar`` function.

Basic Error Bars
~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from plotez import plot_errorbar
   from plotez.backend.utilities import ErrorPlotConfig

   # Generate sample data with errors
   x = np.linspace(0, 10, 20)
   y = np.sin(x)
   x_err = 0.1 * np.random.rand(len(x))
   y_err = 0.1 * np.random.rand(len(y))

   # Simple error bar plot
   plot_errorbar(x, y, x_err=x_err, y_err=y_err)

   # With custom styling
   ep = ErrorPlotConfig(linestyle='--', capsize=5, color='blue')
   plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep)

Enhanced Error Bar Styling
~~~~~~~~~~~~~~~~~~~~~~~~~~

ErrorPlotConfig provides access to all line styling options
plus specialized error bar parameters:

.. code-block:: python

   # Full customization with enhanced error bar styling
   ep = ErrorPlotConfig(
       # Line styling
       linestyle='-',
       linewidth=2,
       color='darkblue',
       marker='o',
       markersize=6,
       alpha=0.7,

       # Error bar specific styling
       capsize=8,           # Length of error bar caps
       elinewidth=2,        # Width of error bar lines
       ecolor='red',        # Color of error bars (can differ from line color)
       capthick=2           # Thickness of error bar caps
   )

   plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep)

Creating ErrorPlotConfig from Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``populate()`` class method to create ErrorPlotConfig instances from parameter dictionaries:

.. code-block:: python

   # Using parameter aliases
   params = {
       'ls': '--',          # linestyle
       'lw': 2,             # linewidth
       'color': 'purple',
       'marker': 's',
       'ms': 6,             # markersize
       'capsize': 7,
       'elinewidth': 2,
       'ecolor': 'crimson'
   }

   ep = ErrorPlotConfig.populate(params)
   plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep)

Error Band Plots
----------------

PlotEZ also supports shaded error band plots through the ``ErrorBandConfig`` class
and the ``plot_errorband`` function.

.. code-block:: python

   import numpy as np
   from plotez import plot_errorband
   from plotez.backend.utilities import ErrorBandConfig, LinePlotConfig

   x = np.linspace(0, 10, 50)
   y = np.sin(x)
   y_low = y - 0.2
   y_upp = y + 0.2

   band_config = ErrorBandConfig(color='cyan', edgecolor='k', linestyle='--', hatch='\\')
   line_config = LinePlotConfig(color='gold', linestyle='--', linewidth=2,
                                marker='o', markersize=5, markeredgecolor='k')

   ax = plot_errorband(x, y, y_low, y_upp,
                       data_label=r'$\sin(x)$',
                       band_config=band_config,
                       line_config=line_config)

Next Steps
----------

* Explore the :doc:`api` for complete function signatures
* Check out the :doc:`CHANGELOG` for version history
* Review the test suite for more usage examples
