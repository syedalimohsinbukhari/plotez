API Reference
=============

This page contains the API reference for PlotEZ.

Main Plotting Functions
-----------------------

.. automodule:: plotez.plotez
   :members:
   :undoc-members:
   :show-inheritance:

Utility Classes
---------------

Parameter Classes
~~~~~~~~~~~~~~~~~

.. autoclass:: plotez.backend.utilities.LinePlot
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: plotez.backend.utilities.ErrorPlot
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::
      ErrorPlot inherits from LinePlot, providing all line plot styling options
      (line_style, line_width, color, alpha, marker properties) plus additional
      error bar styling parameters (capsize, elinewidth, ecolor, capthick).

.. autoclass:: plotez.backend.utilities.ScatterPlot
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: plotez.backend.utilities.SubPlots
   :members:
   :undoc-members:
   :show-inheritance:

Utility Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: plotez.backend.utilities.plot_or_scatter

.. autofunction:: plotez.backend.utilities.plot_dictionary_handler

.. autofunction:: plotez.backend.utilities.split_dictionary

.. autofunction:: plotez.backend.utilities.dual_axes_data_validation

.. autofunction:: plotez.backend.utilities.dual_axes_label_management

Error Handling
--------------

.. automodule:: plotez.backend.error_handling
   :members:
   :undoc-members:
   :show-inheritance:

