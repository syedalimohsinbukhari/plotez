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
       plot_title='Dual Y-Axis Example',
       use_twin_x=True
   )

Dual X-Axis
~~~~~~~~~~~

.. code-block:: python

   plot_xyy(
       x, y1, y2,
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
   from plotez.backend.utilities import LinePlot

   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Create custom line plot parameters
   line_params = LinePlot(
       line_style=['-'],
       line_width=[2],
       color=['#FF5733'],
       marker=['o'],
       marker_size=[4]
   )

   plot_xy(x, y, plot_dictionary=line_params)

Scatter Plots
~~~~~~~~~~~~~

.. code-block:: python

   from plotez.backend.utilities import ScatterPlot

   scatter_params = ScatterPlot(
       color=['blue'],
       size=[50],
       marker=['s'],
       alpha=[0.6]
   )

   plot_xy(x, y, is_scatter=True, plot_dictionary=scatter_params)

Subplot Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from plotez.backend.utilities import SubPlots

   subplot_params = SubPlots(
       share_x=True,
       share_y=True,
       fig_size=(12, 8)
   )

   fig, axs = two_subplots(
       [x, x], [y, y*2],
       orientation='h',
       subplot_dictionary=subplot_params
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

Next Steps
----------

* Explore the :doc:`api` for complete function signatures
* Check out the :doc:`CHANGELOG` for version history
* Review the test suite for more usage examples

