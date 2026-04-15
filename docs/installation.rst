Installation
============

Requirements
------------

PlotEZ requires **Python 3.10 or later** and the following runtime dependencies:

* `matplotlib <https://matplotlib.org>`_ – core plotting engine
* `numpy <https://numpy.org>`_ – numerical array support

Installing from PyPI
--------------------

Using ``pip``:

.. code-block:: bash

   pip install plotez

Using ``uv``:

.. code-block:: bash

   uv add plotez

Installing from Source
----------------------

Using ``pip``:

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e .

Using ``uv``:

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   uv sync

Development Installation
------------------------

Using ``pip``:

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   pip install -e ".[dev]"

Using ``uv`` (recommended):

.. code-block:: bash

   git clone https://github.com/syedalimohsinbukhari/plotez.git
   cd plotez
   uv sync --group dev

This installs the following additional tools:

+--------------------+----------------------------------------+
| Package            | Purpose                                |
+====================+========================================+
| pytest             | Testing framework                      |
+--------------------+----------------------------------------+
| pytest-cov         | Coverage reporting                     |
+--------------------+----------------------------------------+
| mypy               | Static type checking                   |
+--------------------+----------------------------------------+
| black              | Code formatting                        |
+--------------------+----------------------------------------+
| isort              | Import sorting                         |
+--------------------+----------------------------------------+
| flake8             | Style linting                          |
+--------------------+----------------------------------------+
| pydocstyle         | Docstring linting                      |
+--------------------+----------------------------------------+
| pre-commit         | Git hook management                    |
+--------------------+----------------------------------------+
| sphinx             | Documentation generation               |
+--------------------+----------------------------------------+
| sphinx-copybutton  | Copy-button for code blocks            |
+--------------------+----------------------------------------+
| sphinx-rtd-theme   | Read the Docs Sphinx theme             |
+--------------------+----------------------------------------+
| myst-parser        | Markdown support in Sphinx             |
+--------------------+----------------------------------------+
| build              | PEP 517 package builder                |
+--------------------+----------------------------------------+
| tomli              | TOML parsing (Python < 3.11)           |
+--------------------+----------------------------------------+

Verifying Installation
----------------------


.. code-block:: python

   import plotez
   print(plotez.__version__)
