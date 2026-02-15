# PlotEZ

**Mundane plotting made easy.**

PlotEZ is a Python library that simplifies common matplotlib plotting tasks with an intuitive API. Create complex plots with minimal boilerplate code.

## Features

- 🎨 **Simple API**: Create complex plots with just a few lines of code
- 📊 **Dual-Axis Support**: Easy creation of dual y-axis or dual x-axis plots
- 📐 **Multi-Panel Layouts**: Flexible subplot arrangements with automatic labeling
- 📁 **File Integration**: Direct plotting from CSV files
- 🎛️ **Extensive Customization**: Full control over plot appearance via parameter classes
- 🔍 **Type Safety**: Complete type hints for better IDE support and type checking (PEP 561 compliant)
- ✅ **Well Tested**: Comprehensive test suite with 96% coverage

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

# Create plot with automatic labeling
plot_xy(x, y, auto_label=True)
```

## Examples

### Dual Y-Axis Plot

```python
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

### Multi-Panel Plots

```python
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

### Custom Styling

```python
from plotez import plot_xy
from plotez.backend.utilities import LinePlot

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

- ✅ Type hints corrected throughout codebase
- ✅ Test suite implemented (96% coverage)
- ✅ Documentation structure created
- ✅ Development tools configured (pytest, mypy, sphinx)
- ✅ PEP 561 compliance (py.typed marker)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Authors

- Syed Ali Mohsin Bukhari - [ali.mohsin@ist.edu.pk](mailto:ali.mohsin@ist.edu.pk)

## Links

- **Repository**: https://github.com/syedalimohsinbukhari/plotez
- **Issues**: https://github.com/syedalimohsinbukhari/plotez/issues
