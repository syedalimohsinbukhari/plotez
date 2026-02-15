Installation
============

Requirements
------------

PlotEZ requires Python 3.10 or later and depends on:

* matplotlib

Installing from PyPI
--------------------

Once published, you can install plotez using pip:

.. code-block:: bash

   pip install plotez

Installing from Source
----------------------

To install from source:

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e .

Development Installation
------------------------

For development work, install with development dependencies:

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e ".[dev]"

This installs additional tools for testing and documentation:

* pytest - Testing framework
* pytest-cov - Coverage reporting
* mypy - Static type checking
* sphinx - Documentation generation
* sphinx-rtd-theme - ReadTheDocs theme

Verifying Installation
----------------------

To verify the installation:

.. code-block:: python

   import plotez
   print(plotez.__version__)

