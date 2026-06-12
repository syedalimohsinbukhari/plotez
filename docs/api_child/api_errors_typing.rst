Errors and Type Aliases
=======================

Error Handling
--------------

Public exceptions are available from ``plotez.errors``.

Base Exceptions
~~~~~~~~~~~~~~~

.. autoclass:: plotez.errors.PlotEZError
   :show-inheritance:

.. autoclass:: plotez.errors.DataError
   :show-inheritance:

.. autoclass:: plotez.errors.ConfigurationError
   :show-inheritance:

.. autoclass:: plotez.errors.OrientationError
   :show-inheritance:

Data Exceptions
~~~~~~~~~~~~~~~

.. autoclass:: plotez.errors.ShapeError
   :show-inheritance:

.. autoclass:: plotez.errors.DataLengthError
   :show-inheritance:

.. autoclass:: plotez.errors.EmptyDataError
   :show-inheritance:

.. autoclass:: plotez.errors.ColumnCountError
   :show-inheritance:

Configuration Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: plotez.errors.AxisLabelError
   :show-inheritance:

.. autoclass:: plotez.errors.TwinXDataError
   :show-inheritance:

.. autoclass:: plotez.errors.TwinYDataError
   :show-inheritance:

.. autoclass:: plotez.errors.XArrayNot1D
   :show-inheritance:

.. autoclass:: plotez.errors.YArrayNot1D
   :show-inheritance:

Type Aliases
------------

.. note::

   ``AxesReturn`` describes single- and dual-axis plotting results:
   ``Axes | tuple[Axes, Axes]``. Grid functions such as ``n_plotter`` and
   ``two_subplots`` return a shaped ``NDArray`` of ``Axes`` directly.

.. automodule:: plotez.typing
   :members:
   :undoc-members:
   :show-inheritance:
