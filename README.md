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
- **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
- **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling
- **File Integration**: Direct plotting from CSV files
- **Extensive Customization**: Full control over plot appearance via parameter classes
- **Type Safety**: Complete type hints for better IDE support and type checking (PEP 561 compliant)
- **Well Tested**: Comprehensive test suite with 85%+ coverage

## Installation

### From PyPI (once published)

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
import numpy as np
from plotez import plot_xy

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot with automatic labeling
plot_xy(x, y, auto_label=True)
```

![Example1 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/README_example1.png)

## Examples

### Dual Y-Axis Plot

```python
import numpy as np
from plotez import plot_xyy

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(x / 10)

plot_xyy(
    x, y1, y2,
    x_label='Time',
    y1_label='Sine',
    y2_label='Exponential',
    data_labels=['sin(x)', 'exp(x/10)'],
    plot_title='Dual Y-Axis Example',
    use_twin_x=True
)
```

![Example2 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/README_example2.png)

### Multi-Panel Plots

```python
import numpy as np
from plotez import n_plotter

# Create 2×2 grid
x_data = [np.linspace(0, 10, 100) for _ in range(4)]
y_data = [
    np.sin(x_data[0]),
    np.cos(x_data[1]),
    np.tan(x_data[2] / 5),
    x_data[3]**2 / 100
]

fig, axs = n_plotter(
    x_data, y_data,
    n_rows=2, n_cols=2,
    auto_label=True
)
```

![Example3 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/README_example3.png)

### Custom Styling

```python
import numpy as np
from plotez import plot_xy
from plotez.backend.utilities import LinePlot

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create custom line plot parameters
line_params = LinePlot(
    line_style=['-'],
    line_width=[2],
    color=['#FF5733'],
    marker=['o'],
    marker_size=[4]
)

plot_xy(x, y, plot_dictionary=line_params)
```

![Example4 Plot](https://raw.githubusercontent.com/syedalimohsinbukhari/plotez/refs/heads/master/examples/README_example4.png)

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

- Type hints are corrected throughout the codebase
- Test suite implemented (80%+ coverage)
- Documentation structure created
- Development tools configured (pytest, mypy, sphinx)
- PEP 561 compliance (py.typed marker)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License – see [LICENSE](LICENSE) file for details.

## Authors

- Syed Ali Mohsin Bukhari - [ali.mohsin@ist.edu.pk](mailto:ali.mohsin@ist.edu.pk)

## Links

- **Repository**: https://github.com/syedalimohsinbukhari/plotez
- **Issues**: https://github.com/syedalimohsinbukhari/plotez/issues
