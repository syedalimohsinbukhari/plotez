Installation
============

Requirements
------------

PlotEZ requires **Python 3.10 or later** and the following runtime dependencies:

* `matplotlib <https://matplotlib.org>`_ – core plotting engine
* `numpy <https://numpy.org>`_ – numerical array support

Installing from PyPI
--------------------

.. code-block:: bash

   pip install plotez

Installing from Source
----------------------

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e .

Development Installation
------------------------

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e ".[dev]"

This installs the following additional tools:

+------------------+----------------------------------------+
| Package          | Purpose                                |
+==================+========================================+
| pytest           | Testing framework                      |
+------------------+----------------------------------------+
| pytest-cov       | Coverage reporting                     |
+------------------+----------------------------------------+
| mypy             | Static type checking                   |
+------------------+----------------------------------------+
| black            | Code formatting                        |
+------------------+----------------------------------------+
| isort            | Import sorting                         |
+------------------+----------------------------------------+
| flake8           | Style linting                          |
+------------------+----------------------------------------+
| pydocstyle       | Docstring linting                      |
+------------------+----------------------------------------+
| pre-commit       | Git hook management                    |
+------------------+----------------------------------------+
| sphinx           | Documentation generation               |
+------------------+----------------------------------------+
| sphinx-copybutton| Copy-button for code blocks            |
+------------------+----------------------------------------+
| myst-parser      | Markdown support in Sphinx             |
+------------------+----------------------------------------+
| build            | PEP 517 package builder                |
+------------------+----------------------------------------+

Verifying Installation
----------------------


.. code-block:: python

   import plotez
   print(plotez.__version__)
