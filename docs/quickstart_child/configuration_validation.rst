Configuration and Validation
============================

Config objects make styles reusable, while domain-specific exceptions and early validation make invalid inputs predictable.
Complete class signatures, fields, and shorthand tables are available in :doc:`../api`.

.. contents:: Sections
   :local:
   :depth: 1

----

Config Classes
--------------

``LinePlotConfig`` and its siblings ``ErrorPlotConfig``, ``ErrorBandConfig``, ``ScatterPlotConfig``, and
``HistogramConfig`` provide IDE autocomplete and can be reused across plots.
Any matplotlib parameter not covered by a named field can be forwarded through the ``_extra`` dictionary.

.. literalinclude:: ../../examples/rtd_images/RTD_E5-2_errorbar_customized.py
   :language: python
   :lines: 3-33

.. image:: ../../examples/rtd_images/RTD_E5-2_errorbar_customized.png

----

Shorthand Helpers
-----------------

``lpc``, ``epc``, ``ebc``, ``spc``, and ``hgc`` are factory functions that accept familiar matplotlib aliases such as
``c``, ``lw``, ``ls``, ``ms``, ``mec``, and ``mfc`` and return the corresponding config object.

.. code-block:: python

   from plotez import lpc, epc, ebc, spc, hgc

   line = lpc(c='steelblue', lw=2, ls='--', marker='o', ms=4)
   ep = epc(c='darkblue', ls=':', lw=2, marker='d', ms=6, capsize=8, elinewidth=2, ecolor='red')
   band = ebc(c='cyan', alpha=0.3, ec='k', ls='--', hatch='/')
   dots = spc(c='orange', s=40, alpha=0.7, marker='^')
   hist = hgc(bins=40, c='steelblue', ec='white', alpha=0.8)

See the :ref:`shorthand-key-reference` for every supported alias.

----

Exception Hierarchy
-------------------

PlotEZ provides domain-specific exceptions for clear, catchable error handling.
All public exceptions are available from ``plotez.errors``.

.. code-block:: text

   PlotEZError
   +-- OrientationError
   +-- DataError
   |   +-- ShapeError
   |   +-- DataLengthError
   |   +-- EmptyDataError
   |   +-- ColumnCountError
   +-- ConfigurationError
       +-- AxisLabelError
       +-- TwinXDataError
       +-- TwinYDataError
       +-- XArrayNot1D
       +-- YArrayNot1D

Catch a specific exception when recovery depends on the failure:

.. code-block:: python

   import numpy as np
   from plotez import plot_errorbar
   from plotez.errors import ShapeError

   x = np.array([1, 2, 3])
   y = np.array([1, 2, 3])
   bad_err = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

   try:
       plot_errorbar(x, y, x_err=bad_err)
   except ShapeError as error:
       print(f"Invalid error array: {error}")

Use ``DataError`` or ``ConfigurationError`` when one handler can cover a related group of failures.
The :doc:`../api` reference documents each exception.

----

Shape and Length Validation
---------------------------

Public plotting functions validate inputs before calling matplotlib.
Data arrays that represent a single series must be one-dimensional, arrays that align must have equal lengths, and
asymmetric error arrays must have shape ``(2, N)``.

``ShapeError`` reports invalid dimensionality or error-array shape.
``DataLengthError`` separately reports arrays that do not align:

.. code-block:: python

   from plotez import plot_xy
   from plotez.errors import DataLengthError

   try:
       plot_xy([1, 2, 3], [10, 20])
   except DataLengthError as error:
       print(f"Data does not align: {error}")

Grid functions also validate that the provided data fits the requested grid, and file plotting validates row and column
counts before plotting.

----

Label Collections
-----------------

Label parameters such as ``data_labels``, ``x_labels``, ``y_labels``, ``subplot_titles``, and ``axis_labels`` accept
either a ``list[str]`` or ``tuple[str, ...]``. Both forms behave the same, and PlotEZ copies the provided collection
before any internal normalization. Defaults remain ``None`` to avoid mutable default arguments.

.. code-block:: python

   from plotez import two_subplots

   axs = two_subplots(
       x_list,
       y_list,
       x_labels=["Time (s)", "Time (s)"],
       y_labels=("Amplitude", "Phase"),
   )
