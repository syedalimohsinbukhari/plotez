# Changelog

All notable changes to plotez will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Error Bar Plotting**: Complete error bar plotting functionality with `plot_errorbars` function
- **ErrorPlot Class**: New parameter class for error bar plot customization
  - Inherits from `LinePlot` for consistent line styling
  - Additional error bar parameters: `capsize`, `elinewidth`, `ecolor`, `capthick`
  - `populate()` class method for creating instances from dictionaries
  - Full compatibility with all LinePlot styling options

### Enhanced
- **ErrorPlot Inheritance**: ErrorPlot now properly inherits from LinePlot
  - Eliminates code duplication between line plots and error bar plots
  - Automatic access to all line styling parameters (line_style, line_width, color, alpha, marker properties)
  - Enhanced error bar styling with independent control over error bar appearance
- **Documentation**: Updated API documentation and quickstart guide with comprehensive error bar examples
- **Code Quality**: Improved maintainability through inheritance-based design

### Fixed
- Dictionary iteration issues in `plot_dictionary_handler()` function
- Parameter consistency between LinePlot and ErrorPlot classes

## [v0.1.1]
### Changed
- Path change for examples and images
- Updated README
- Updated type hints
- Simplified parameter handling in `ScatterPlot` and `LinePlot` w.r.t. `_PlotParams`
- Updated `pyproject.toml` with classifiers and removed commented URLs.
- Fixed parameter formatting to improve code readability.
- Adjusted GitHub Actions workflows (`black` linting and naming).

## [v0.1.0] - 2026-02-01 13:04 PM

### Added

- Initial release – Refactored and rebranded from the `mpyez` project
- Core plotting functions:
    - `plot_xy`: Simple x vs. y plotting with extensive customization
    - `plot_xyy`: Dual-axis plotting (dual y-axis or dual x-axis)
    - `plot_with_dual_axes`: Flexible single or dual-axis plotting
    - `two_subplots`: Create two subplots (horizontal or vertical orientation)
    - `n_plotter`: Create n$\times$m grid of subplots
    - `plot_two_column_file`: Direct CSV file plotting
- Parameter classes for plot customization:
    - `LinePlot`: Line plot parameters (line style, width, color, markers, etc.)
    - `ScatterPlot`: Scatter plot parameters (colors, sizes, markers, etc.)
    - `SubPlots`: Subplot configuration (figure size, axis sharing)
- Custom exceptions:
    - `PlotError`: Base exception for plotting errors
    - `OrientationError`: Exception for invalid subplot orientation
- Comprehensive test suite with 70%+ code coverage
- Type hints throughout the codebase (PEP 561 compliant with py.typed marker)
- Development tools integration:
    - pytest for testing
    - pytest-cov for coverage reporting
    - mypy for static type checking
    - Sphinx for documentation generation

## [0.1.0] - 2026-02-01 11:55 AM

### Notes

- First official release of plotez
- Evolved from the mpyez project with improved architecture and API

