Error Visualization
===================

Use error bars for discrete measurements and shaded bands for dense, continuous data.
Complete signatures and parameter details are available in :doc:`../api`.

.. contents:: Sections
   :local:
   :depth: 1

----

Basic Error Bars
----------------

``y_err`` (and ``x_err``) can be a scalar (same error everywhere) or an array
(per-point errors). A 1D error array must match the corresponding data length;
asymmetric errors must have shape ``(2, N)``. Invalid shapes raise ``ShapeError``
and incompatible lengths raise ``DataLengthError`` before matplotlib is called.
Caps are shown by default and controlled via ``capsize``.

.. literalinclude:: ../../examples/rtd_images/RTD_E4_errorbar.py
   :language: python
   :lines: 3-15

.. image:: ../../examples/rtd_images/RTD_E4_errorbar.png

----

Styled Error Bars
-----------------

``ErrorPlotConfig`` exposes line styling options plus specialized error bar
parameters. ``ecolor`` sets the error bar colour independently from the line colour;
``elinewidth`` sets the error bar line thickness.

.. literalinclude:: ../../examples/rtd_images/RTD_E5_errorbar_customized.py
   :language: python
   :lines: 3-32

.. image:: ../../examples/rtd_images/RTD_E5_errorbar_customized.png

----

Asymmetric Errors
-----------------

Pass a ``(2, N)`` array to ``y_err`` (or ``x_err``) for different lower and upper
uncertainties: the first row contains lower errors and the second contains upper
errors.

.. literalinclude:: ../../examples/rtd_images/RTD_E6_asym_errors.py
   :language: python
   :lines: 3-14

.. image:: ../../examples/rtd_images/RTD_E6_asym_errors.png

----

Absolute Error Bands
--------------------

For dense, continuous data shaded bands are cleaner than individual error bars.
``y_lower`` and ``y_upper`` are absolute values (not offsets); ``band_config``
controls the fill and ``line_config`` controls the central line. Array-valued
bounds must be 1D and have the same length as ``x_data`` and ``y_data``.

.. literalinclude:: ../../examples/rtd_images/RTD_E7_errorbands.py
   :language: python
   :lines: 3-26

.. image:: ../../examples/rtd_images/RTD_E7_errorbands.png

----

Relative Error Bands
--------------------

``plot_errorband_relative`` is a convenience wrapper around ``plot_errorband`` where
``y_lower`` and ``y_upper`` are offsets from ``y_data`` rather than absolute bounds.
You can pass a single uncertainty value and let plotEZ compute the band edges.
Array-valued offsets must be 1D and match the length of ``y_data``.

.. literalinclude:: ../../examples/rtd_images/RTD_E15_errorband_relative.py
   :language: python
   :lines: 3-25

.. image:: ../../examples/rtd_images/RTD_E15_errorband_relative.png
