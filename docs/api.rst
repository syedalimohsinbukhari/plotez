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

.. autoclass:: plotez.backend.utilities.LinePlotConfig
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: plotez.backend.utilities.ErrorPlotConfig
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: plotez.backend.utilities.ErrorBandConfig
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: plotez.backend.utilities.ScatterPlotConfig
   :members:
   :undoc-members:
   :show-inheritance:


Utility Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: plotez.backend.utilities.plot_or_scatter

.. autofunction:: plotez.backend.utilities.split_dictionary

.. autofunction:: plotez.backend.utilities.dual_axes_data_validation

.. autofunction:: plotez.backend.utilities.dual_axes_label_management

Convenience / Wrapper Functions
--------------------------------

These factory functions provide a concise, keyword-driven way to build config objects without
importing the dataclass names directly. All are available at the top-level ``plotez`` namespace.

Each function also has a **short alias** that can be used interchangeably:

+------------------------------+---------------+
| Long-form function           | Short alias   |
+==============================+===============+
| ``line_plot_configuration``  | ``lpc``       |
+------------------------------+---------------+
| ``error_plot_configuration`` | ``epc``       |
+------------------------------+---------------+
| ``error_band_configuration`` | ``ebc``       |
+------------------------------+---------------+
| ``scatter_plot_configuration``| ``spc``      |
+------------------------------+---------------+

.. autofunction:: plotez.backend._wrappers.line_plot_configuration

.. autofunction:: plotez.backend._wrappers.error_plot_configuration

.. autofunction:: plotez.backend._wrappers.error_band_configuration

.. autofunction:: plotez.backend._wrappers.scatter_plot_configuration

.. _shorthand-key-reference:

Shorthand Key Reference
-----------------------

All ``populate()`` class methods and wrapper functions accept shorthand aliases in place of full
matplotlib parameter names. The tables below list every recognised alias.

Line / Error-bar parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------+---------------------+
| Alias    | Full parameter name |
+==========+=====================+
| ``ls``   | ``linestyle``       |
+----------+---------------------+
| ``lw``   | ``linewidth``       |
+----------+---------------------+
| ``c``    | ``color``           |
+----------+---------------------+
| ``ms``   | ``markersize``      |
+----------+---------------------+
| ``mec``  | ``markeredgecolor`` |
+----------+---------------------+
| ``mfc``  | ``markerfacecolor`` |
+----------+---------------------+
| ``mew``  | ``markeredgewidth`` |
+----------+---------------------+

Error-bar-only parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ErrorPlotConfig`` / ``epc`` wrapper also accepts all line aliases above, plus:

+----------------+---------------------+
| Alias          | Full parameter name |
+================+=====================+
| ``ecolor``     | ``ecolor``          |
+----------------+---------------------+
| ``elinewidth`` | ``elinewidth``      |
+----------------+---------------------+
| ``capsize``    | ``capsize``         |
+----------------+---------------------+
| ``capthick``   | ``capthick``        |
+----------------+---------------------+

Scatter parameters
~~~~~~~~~~~~~~~~~~

+--------+---------------------+
| Alias  | Full parameter name |
+========+=====================+
| ``c``  | ``color``           |
+--------+---------------------+
| ``s``  | ``size``            |
+--------+---------------------+
| ``ec`` | ``edgecolors``      |
+--------+---------------------+
| ``fc`` | ``facecolors``      |
+--------+---------------------+

Error Handling
--------------

.. automodule:: plotez.backend.error_handling
   :members:
   :undoc-members:
   :show-inheritance:

Type Aliases
------------

.. automodule:: plotez.typing
   :members:
   :undoc-members:
   :show-inheritance:
