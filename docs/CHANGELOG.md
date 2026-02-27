# Changelog

All notable changes to plotez will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.2.0] - 27-Feb-2026

### Added
- **Error Bar Plotting**: `plot_errorbar` function for error bar plots with full customization
- **Error Band Plotting**: `plot_errorband` function for shaded error band visualization
- **ErrorPlotConfig**: Dataclass for error bar plot styling (color, capsize, ecolor, elinewidth, capthick, etc.)
- **ErrorBandConfig**: Dataclass for error band styling (color, alpha, hatch, edgecolor, interpolate, etc.)
- Comprehensive test suites for `plot_errorbar` and `plot_errorband`
- `plot_errorband` and all config classes exported from `plotez` top-level package
- `CHANGELOG.md` symlink at repository root for GitHub visibility

### Changed
- **Renamed parameter classes** (breaking):
  - `LinePlot` → `LinePlotConfig`
  - `ScatterPlot` → `ScatterPlotConfig`
  - `FigureConfig` field names now use matplotlib-native names (`figsize`, `sharex`, `sharey` instead of `fig_size`, `share_x`, `share_y`)
- **Renamed function keyword arguments** (breaking):
  - `plot_dictionary` → `plot_config`
  - `subplot_dictionary` / `subplot_config` → `figure_config`
- All parameter classes converted to `dataclasses` with `_extra` dict for arbitrary kwargs
- `populate()` class methods on all config classes for alias-based dictionary creation
- Replaced `typing.Tuple` / `typing.List` with built-in `tuple` / `list` generics (Python >= 3.10)
- Added type annotation `Axes | None` to `plot_xyy`'s `axis` parameter
- Added `Returns` sections to all public function docstrings
- Added `Attributes` sections to all config dataclass docstrings
- Updated `quickstart.rst`, `api.rst`, and `README.md` to reflect current API
- Excluded `md_SUMMARIES/` from package builds

### Fixed
- Tests using non-existent `subplot_config` kwarg (→ `figure_config`)
- `quickstart.rst` referencing old `LinePlot`, `ScatterPlot`, `plot_errorbars`, `plot_dictionary`, `subplot_dictionary`
- `README.md` referencing old `LinePlot`, `line_style`, `marker_size`, `mark_every`
- `api.rst` stale note about ErrorPlotConfig inheriting from LinePlotConfig

## [v0.1.1] 16-Feb-2026
### Changed
- Path change for examples and images
- Updated README
- Updated type hints
- Simplified parameter handling in `ScatterPlot` and `LinePlot` w.r.t. `_PlotParams`
- Updated `pyproject.toml` with classifiers and removed commented URLs.
- Fixed parameter formatting to improve code readability.
- Adjusted GitHub Actions workflows (`black` linting and naming).

## [v0.1.0] - 16-Feb-2026

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
    - `FigureConfig`: Subplot configuration (figure size, axis sharing)
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

### Notes

- First official release of plotez
- Evolved from the mpyez project with improved architecture and API
