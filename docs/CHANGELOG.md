# Changelog

All notable changes to plotez will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release - Refactored and rebranded from mpyez project
- Core plotting functions:
  - `plot_xy`: Simple x vs y plotting with extensive customization
  - `plot_xyy`: Dual-axis plotting (dual y-axis or dual x-axis)
  - `plot_with_dual_axes`: Flexible single or dual-axis plotting
  - `two_subplots`: Create two subplots (horizontal or vertical orientation)
  - `n_plotter`: Create n×m grid of subplots
  - `plot_two_column_file`: Direct CSV file plotting
- Parameter classes for plot customization:
  - `LinePlot`: Line plot parameters (line style, width, color, markers, etc.)
  - `ScatterPlot`: Scatter plot parameters (colors, sizes, markers, etc.)
  - `SubPlots`: Subplot configuration (figure size, axis sharing)
- Custom exceptions:
  - `PlotError`: Base exception for plotting errors
  - `NoXYLabels`: Exception for missing axis labels
  - `OrientationError`: Exception for invalid subplot orientation
- Comprehensive test suite with 70%+ code coverage
- Type hints throughout the codebase (PEP 561 compliant with py.typed marker)
- Development tools integration:
  - pytest for testing
  - pytest-cov for coverage reporting
  - mypy for static type checking
  - Sphinx for documentation generation

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

## [0.1.0] - YYYY-MM-DD

### Notes
- First official release of plotez
- Evolved from the mpyez project with improved architecture and API

