# plotEZ

**Mundane plotting made easy.**

![GitHub Release](https://img.shields.io/github/v/release/syedalimohsinbukhari/plotez?color=magenta)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/plotez?)
![GitHub-licence](https://img.shields.io/github/license/syedalimohsinbukhari/plotez?color=darkblue)
![GiHub-CodeCoverage](https://img.shields.io/codecov/c/github/syedalimohsinbukhari/plotez?color=cyan)
![GitHub top language](https://img.shields.io/github/languages/top/syedalimohsinbukhari/plotez?color=lightgreen)
![GitHub contributors](https://img.shields.io/github/contributors/syedalimohsinbukhari/plotez?color=gold)
![Github Issues](https://img.shields.io/github/issues/syedalimohsinbukhari/plotez?color=orange)
![GitHub OPEN PRs](https://img.shields.io/github/issues-pr/syedalimohsinbukhari/plotez?color=darkred)
![GitHub CLOSED PRs](https://img.shields.io/github/issues-pr-closed/syedalimohsinbukhari/plotez?color=darkgreen)

`plotez` is a Python library that simplifies common matplotlib plotting tasks with an intuitive API. Create complex plots
with minimal boilerplate code.

## Features

- **Simple API**: Create complex plots with just a few lines of code
- **Error Bar Plotting**: Comprehensive error bar support with enhanced styling options
- **Error Band Plotting**: Shaded error band support via `plot_errorband` and `ErrorBandConfig`
- **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
- **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling
- **File Integration**: Direct plotting from CSV files
- **Extensive Customization**: Full control over plot appearance via parameter classes
- **Type Safety**: Complete type hints for better IDE support and type checking (PEP 561 compliant)
- **Well Tested**: Comprehensive test suite with 85%+ coverage

## Installation

### From PyPI

```bash
pip install plotez
```

### From Source

```bash
git clone https://github.com/syedalimohsinbukhari/plotez.git
cd plotez
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
"""Basic plotting example."""

import numpy as np
from plotez import plot_xy

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot with automatic labeling
plot_xy(x, y, auto_label=True)
```

![Example1 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example1.png)

## Examples

### Dual Y-Axis Plot

```python
"""Demonstration of dual-y axis capability."""

import numpy as np
from plotez import plot_xyy

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(-x / 10)

plot_xyy(x, y1, y2,
         x_label="Time", y1_label="Sine", y2_label="Exponential",
         data_labels=["sin(x)", "exp(-x/10)"], plot_title="Dual Y-Axis Example")
```

![Example2 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example2.png)


```python
"""Demonstration of dual-y axis capability with custom plot configuration."""

import matplotlib.pyplot as plt
import numpy as np

from plotez import plot_xyy
from plotez.backend import LinePlotConfig

x = np.linspace(0, 10, 50)
y1 = np.sin(x)
y2 = np.exp(-x / 10)

plot_config = LinePlotConfig(linestyle=["--", "-."], color=["red", "cyan"], marker=["o", "s"],
                             markersize=[10, 10], markeredgecolor=["k", "k"], _extra={"markevery": [3, 5]})

plot_xyy(x, y1, y2,
         x_label="Time", y1_label="Sine", y2_label="Exponential", data_labels=["sin(x)", "exp(-x/10)"],
         plot_config=plot_config)
```

![Example2A Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example2A.png)

### Multi-Panel Plots

```python
"""Demonstration of multi-panel layout capability with customizations."""

import numpy as np
from plotez import n_plotter
from plotez.backend import LinePlotConfig, FigureConfig

# Create 2×2 grid
x_data = [np.linspace(0, 10, 100) for _ in range(6)]
y_data = [
    np.sin(x_data[0]),
    np.cos(x_data[1]),
    np.tan(x_data[2] / 5),
    x_data[3]**2 / 100,
    1 / np.cos(x_data[4]),
    x_data[5]
]

line_config = LinePlotConfig(color=["red", "blue", "green", "black", "orange", "magenta"])
fig_config = FigureConfig(figsize=(10, 6))

fig, axs = n_plotter(x_data, y_data,
                     n_rows=2, n_cols=3, auto_label=True,
                     plot_config=line_config, figure_config=fig_config)
```

![Example3 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example3.png)

### Error Bar Plots

```python
import numpy as np

from plotez import plot_errorbar, epc

# Generate sample data with errors
x = np.linspace(0, 10, 20)
x_err = 0.4
y = np.sin(x)
y_err = 0.1 * np.random.rand(len(y))

# Build config with the epc() convenience wrapper (short aliases accepted)
ep = epc(
    ls=':',
    lw=2,
    c='darkblue',
    marker='d',
    ms=6,
    capsize=8,
    elinewidth=2,  # error bar line width
    ecolor='red',  # error bar colour (different from the line!)
    capthick=2,
)
plot_errorbar(x, y, x_err=x_err, y_err=y_err, errorbar_config=ep)
```
![Example4 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example4.png)

### Error Band Plots

```python
"""Demonstration of error band plotting with custom configurations."""
import numpy as np

from plotez import plot_errorband
from plotez.backend import ErrorBandConfig, LinePlotConfig

rng = np.random.default_rng(1234)

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_low = y - 0.2
y_upp = y + 0.2

error_config = ErrorBandConfig(color="cyan", edgecolor="k", linestyle="--", hatch="\\")
line_config = LinePlotConfig(color="gold", linestyle="--", linewidth=2,
                             marker="o", markersize=5, markeredgecolor="k")

ax = plot_errorband(x, y, y_low, y_upp,
                    data_label=r"$\sin(X)$", band_config=error_config, line_config=line_config)
```
![Example5 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/images/README_example5.png)

## Development

### Running Tests

```bash
pytest
```

### With Coverage Report

```bash
pytest --cov=src/plotez --cov-report=html
```

### Type Checking

```bash
mypy src/plotez
```

### Building Documentation

```bash
cd docs
make html
```

## Project Status

| Item           | Status                                                         |
|----------------|----------------------------------------------------------------|
| Latest version | v0.2.0                                                         |
| Python support | 3.10 · 3.11 · 3.12                                             |
| Test coverage  | 85%+                                                           |
| Type hints     | ✅ PEP 561 compliant (`py.typed`)                               |
| Documentation  | [Read the Docs](https://plotez.readthedocs.io) *(coming soon)* |
| License        | MIT                                                            |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License – see [LICENSE](LICENSE) file for details.

## Authors

- Syed Ali Mohsin Bukhari - [ali.mohsin@ist.edu.pk](mailto:ali.mohsin@ist.edu.pk)

## Links

- **Repository**: https://github.com/syedalimohsinbukhari/plotez
- **Issues**: https://github.com/syedalimohsinbukhari/plotez/issues
