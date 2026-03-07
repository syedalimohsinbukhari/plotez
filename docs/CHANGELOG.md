# Changelog

All notable changes to plotez will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Top-level wrapper aliases**: `lpc`, `epc`, `ebc`, `spc`, `fgc` and their long-form equivalents
  (`line_plot_configuration`, `error_plot_configuration`, `error_band_configuration`,
  `scatter_plot_configuration`, `figure_configuration`) are now exported from the top-level
  `plotez` namespace — no need to import from `plotez.backend` directly
- **`docs/api.rst`** — new "Convenience / Wrapper Functions" section with alias table and
  `autofunction` directives for all five wrapper functions
- **`docs/api.rst`** — new "Shorthand Key Reference" section with RST tables documenting every
  accepted alias for line, error-bar, scatter, and figure parameters
- **`docs/quickstart.rst`** — new "Convenience / Wrapper Functions" section with before/after
  examples showing `epc()`, `lpc()`, `fgc()`, `ebc()`, and `spc()`

### Changed

- **`docs/index.rst`** — Quick Example updated to use current API (`plot_errorbar` + `epc()`) instead of old `plot_errorbars` + `LinePlot` dict
- **`Project Status`** section replaced with a concise Markdown status table (version, Python support, coverage, docs link, license)
- **`docs/installation.rst`** — Requirements section corrected to list actual runtime deps
  (`matplotlib`, `numpy`)
  - a dev-dependency list replaced with a full table matching `requirements-dev.txt` (adds `black`, `isort`, `flake8`, `pydocstyle`, `pre-commit`, `sphinx-copybutton`, `myst-parser`, `build`
- **`README.md`** — "Project Status" section replaced with a concise Markdown status table (version, Python support, coverage, docs link, license); Error Bar Plots example updated to use `epc()` with shorthand keyword aliases

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
    - `FigureConfig` field names now use matplotlib-native names (`figsize`, `sharex`, `sharey` instead of `fig_size`,
      `share_x`, `share_y`)
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
