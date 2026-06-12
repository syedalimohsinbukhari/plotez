Wrappers and Shorthand Keys
===========================

These factory functions provide a concise, keyword-driven way to build config
objects without importing the dataclass names directly. All are available from
the top-level ``plotez`` namespace.

Wrapper Functions
-----------------

Each function has a short alias that can be used interchangeably:

+-------------------------------+-------------+
| Long-form function            | Short alias |
+===============================+=============+
| ``line_plot_configuration``   | ``lpc``     |
+-------------------------------+-------------+
| ``error_plot_configuration``  | ``epc``     |
+-------------------------------+-------------+
| ``error_band_configuration``  | ``ebc``     |
+-------------------------------+-------------+
| ``scatter_plot_configuration``| ``spc``     |
+-------------------------------+-------------+
| ``histogram_config``          | ``hgc``     |
+-------------------------------+-------------+

.. autofunction:: plotez.line_plot_configuration

.. autofunction:: plotez.error_plot_configuration

.. autofunction:: plotez.error_band_configuration

.. autofunction:: plotez.scatter_plot_configuration

.. autofunction:: plotez.histogram_config

.. _shorthand-key-reference:

Shorthand Key Reference
-----------------------

All ``populate()`` class methods and wrapper functions accept shorthand aliases
in place of full matplotlib parameter names.

Line and Error-Bar Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Error-Bar-Only Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

``ErrorPlotConfig`` and ``epc`` also accept:

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

Scatter Parameters
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

Error Band Parameters
~~~~~~~~~~~~~~~~~~~~~

+--------+---------------------+
| Alias  | Full parameter name |
+========+=====================+
| ``c``  | ``color``           |
+--------+---------------------+
| ``ec`` | ``edgecolor``       |
+--------+---------------------+
| ``lw`` | ``linewidth``       |
+--------+---------------------+
| ``ls`` | ``linestyle``       |
+--------+---------------------+

``hatch``, ``interpolate``, and ``step`` pass through under their own names.

Histogram Parameters
~~~~~~~~~~~~~~~~~~~~

+--------+---------------------+
| Alias  | Full parameter name |
+========+=====================+
| ``c``  | ``color``           |
+--------+---------------------+
| ``lw`` | ``linewidth``       |
+--------+---------------------+
| ``ec`` | ``edgecolor``       |
+--------+---------------------+

``bins``, ``density``, ``histtype``, ``alpha``, ``facecolor``, ``orientation``,
``cumulative``, and ``hatch`` pass through under their own names.
