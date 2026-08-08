# Changelog

All notable changes to plotez will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Starting with v0.3.3, each release lists incompatible API or behavior changes under a dedicated **Breaking Changes** heading.

## [v0.4.0] - [UNDER CONSTRUCTION]

### Breaking Changes

- **Configuration import paths cleaned up**: Config classes are no longer re-exported from `plotez.backend` or `plotez.backend.utilities`. Import them from `plotez` for the public convenience API or from `plotez.configurations` for the canonical module path.
- **Wrapper module path cleaned up**: Wrapper helpers now live in `plotez.backend.wrappers`; the old private `plotez.backend._wrappers` module has been removed. The top-level `plotez` wrapper imports remain supported.
- **Backend package re-exports reduced**: `plotez.backend` no longer re-exports config classes or wrapper helpers. Import utilities from `plotez.backend` only when using backend validation or dispatch helpers directly.
- **Styling is off by default**: `plotez` no longer applies its publication-ready `rcParams` convention automatically on import. Previously, importing `plotez` silently mutated matplotlib's global style for the whole process. Call `plotez.enable_style()` explicitly to opt in, or set `PLOTEZ_AUTO_STYLE=1` (or `true`/`yes`) before `import plotez` to restore the previous always-on behavior.

### Added

- **`enable_style()` / `disable_style()`**: New public functions (`plotez._plotez_constants`, re-exported from top-level `plotez`). `enable_style(grid=True)` (re-)applies plotez's convention; `disable_style()` calls `plt.rcdefaults()`.
- **`grid` kwarg on `update_style()` / `enable_style()`**: `grid=False` keeps every other styling choice but leaves `axes.grid` off.
- **`PLOTEZ_AUTO_STYLE` environment variable**: set to `1`/`true`/`yes` before `import plotez` to apply the styling convention automatically on import.
- **Examples**: `examples/ex_images/README_E8_style_comparison.py` and `examples/rtd_images/RTD_E16_style_comparison.py` — 3-panel comparisons of default vs. `enable_style()` vs. `disable_style()`/`enable_style(grid=False)`.

### Changed

- **Version bump**: Updated package version from `v0.3.3post1` to `v0.4.0`.
- **Docs and examples**: Updated config examples to use top-level `plotez` imports.

### Fixed

- **Twin-axis double grid**: `plot_with_dual_axes` now calls `ax2.grid(False)` on `twinx()`/`twiny()` axes to avoid a second, misaligned grid overlay when plotez's style convention has grid enabled.

## [v0.3.3/v0.3.3.post1] - 12-Jun-2026

### Added

- **`DataLengthError` exception**: New `DataError` subclass for arrays that must have matching lengths. It is available from the new `plotez.errors` module.
- **`XArrayNot1D` / `YArrayNot1D` exceptions**: Added specialized `ConfigurationError` subclasses for identifying invalid x- and y-array dimensionality. Public plotting guards now consistently report these failures through the broader `ShapeError` data exception.
- **Shared validation utilities**: Added and exported `validate_1d` and `validate_equal_length`, with dedicated helpers for error-bar arrays, absolute error-band bounds, and relative error-band offsets.
- **Validation guards across plotting functions**:
  - `plot_xy`, `plot_xyy`, `plot_xxy`, and direct `plot_with_dual_axes` calls now reject non-1D or mismatched data.
  - `plot_errorbar` validates x/y data plus scalar, 1D symmetric, and `(2, N)` asymmetric error inputs.
  - `plot_errorband` and `plot_errorband_relative` validate data, bounds, offsets, and inferred-band lengths before performing NumPy arithmetic or calling matplotlib.
  - `plot_hist` and `plot_density` now require a 1D `x_data` array.
  - `n_plotter` now reports insufficient x/y datasets for the requested grid before indexing them.
  - `plot_two_column_file` now raises `EmptyDataError` for empty or single-row files instead of leaking NumPy indexing errors.
- **Validation regression tests**: Added coverage for each guarded plotting path, including happy paths and the regression where a 2D `plot_xy` input must raise `ShapeError` before matplotlib is called.
- **Dedicated exception namespace**: Added `plotez.errors` as the sole public exception module. Import exceptions with statements such as `from plotez.errors import ShapeError`; tracebacks and documentation now use names such as `plotez.errors.ShapeError`.

### Breaking Changes

- **Histogram input contract**: `plot_hist` and `plot_density` no longer accept a 2D array as multiple histogram datasets; callers must provide one 1D dataset per call.
- **Validation error reporting**: Invalid shapes now raise `ShapeError`, incompatible lengths raise `DataLengthError`, and empty file data raises `EmptyDataError`, replacing downstream matplotlib, NumPy, or indexing exceptions with errors that identify the relevant argument.
- **`PlotError` → `PlotEZError`**: The base exception class has been renamed to avoid shadowing the common `PlotError` name in user code. All subclasses (`OrientationError`, `DataError`, `ConfigurationError`, etc.) now inherit from `PlotEZError`. Code that catches `PlotError` must be updated.
- **`AxesReturn` type alias simplified**: `NDArray` removed from the union; the alias is now `Axes | tuple[Axes, Axes]` only, matching the actual return types of all public functions.
- **Exception module**: All exceptions now live exclusively in `plotez.errors`. Imports through the top-level package, `plotez.backend`, and the removed `plotez.backend.error_handling` module are no longer supported.

### Changed

- **`plot_with_dual_axes` scatter default**: When `plot_config=None` and `is_scatter=True`, the function now correctly defaults to `ScatterPlotConfig()` instead of `LinePlotConfig()`.

### Fixed

- **Backend circular import**: Validation utilities now import `ConfigurationError` directly from `plotez.errors`, avoiding partially initialized backend modules while preserving the intended exception for missing error-band bounds.
- **Label collection normalization**: Label parameters continue to accept both `list[str]` and `tuple[str, ...]` without deprecation. Grid labels are copied before padding or trimming, fixing short tuple inputs and preventing mutation of caller-provided lists.

### Infrastructure

- **`requirements.txt` split**: `requirements.txt` now contains base runtime dependencies only (`uv export --no-group dev`); a new `requirements[dev].txt` holds the full pinned dev environment (`uv export`), matching how `pip install -e ".[dev]"` consumers vs. CI consumers use the files.
- **Pre-commit hooks added**: `.pre-commit-config.yaml` gains two new local hooks — `check-version-sync` (runs `scripts/check_version_sync.py` to assert `README.md` matches `version.py`) and `uv-export` (runs `uv lock --upgrade && uv sync` then regenerates both requirements files on every commit). The duplicate `pytest` hook entry was also removed.

## [v0.3.2/v0.3.2.post1] - 20-May-2026

### Fixed

- **Mutable default arguments**: `data_labels`, `x_labels`, `y_labels`, `subplot_titles`, and `axis_labels` parameters in `plot_xyy`, `plot_xxy`, `two_subplots`, and `plot_with_dual_axes` used bare `list` literals as defaults — the classic Python mutable-default bug. All replaced with `None`; intended defaults are assigned inside the function body, narrowing the type to `list[str]` immediately so downstream code has no `| None` complaints.
- **Ghost `auto_label` docstring content**: Removed all references to the non-existent `auto_label` parameter from the docstrings of `plot_errorbar`, `plot_with_dual_axes`, and `plot_hist`.
- **Dead `_auto_handler` function**: Removed from `src/plotez/backend/utilities.py`; it was defined but never called anywhere in the codebase. Its sole dependency `LabelConflictWarning` import was also cleaned up from that module.
- **Internal `tight_layout` calls**: Removed `plt.tight_layout()` from `plot_with_dual_axes` and `fig.tight_layout()` from `n_plotter`. Layout management is now fully at the caller's discretion.

### Changed

- **Axes-only returns** (**Breaking**): All plot functions now return `Axes` (single-axis) or `tuple[Axes, Axes]` (dual-axis) — never `(Figure, Axes)`. Figures are always accessible via `ax.get_figure()`. `n_plotter` and `two_subplots` return a shaped `(n_rows, n_cols)` `ndarray` of `Axes` instead of `(Figure, flat_ndarray)`.
- **`subplot_title` → `subplot_titles`** (**Breaking**): The parameter in `n_plotter` and `two_subplots` has been renamed from `subplot_title` (singular) to `subplot_titles` (plural) to match the `_label_sanitizer` internal keyword and improve consistency.
- **`AxesFigReturn` type alias retired**: `AxesFigReturn` in `src/plotez/typing.py` is now a deprecated alias for `AxesReturn` and will be removed in a future release. `AxesReturn` is extended to `Axes | tuple[Axes, Axes] | NDArray` to cover all return shapes uniformly.
- **Internal list literals → tuples**: All internal calls that constructed `axis_labels=[...]` before passing to `plot_with_dual_axes` (in `plot_xy`, `plot_xyy`, `plot_xxy`) now use `tuple` literals, eliminating spurious `DeprecationWarning`s from within the library itself.
- **Examples**: Updated all examples to use correct return types.

## [v0.3.1] - 17-May-2026

### Fixed

- **RTD build**: Updated `requirements.txt` (pinned Sphinx, `myst-parser`, and related dependencies) to resolve a ReadTheDocs build failure introduced after the `0.3.0` release

## [v0.3.0] - 17-May-2026

### Added

- **Histogram Plotting**: `plot_hist` function for histogram visualisation with full `ax.hist` parameter coverage
- **Density Plotting**: `plot_density` function — a thin wrapper around `plot_hist` that enforces `density=True` for probability-density histograms
- **Relative Error Band**: `plot_errorband_relative` — a convenience wrapper around `plot_errorband` where `y_lower` / `y_upper` are relative offsets from `y_data` rather than absolute bounds
- **`HistogramConfig`**: New dataclass for histogram styling (`bins`, `density`, `histtype`, `color`, `alpha`, `edgecolor`, `facecolor`, `linewidth`, `orientation`, `cumulative`, `hatch`); exported from the top-level `plotez` namespace
- **`histogram_config` / `hgc`**: New convenience factory function (and its short alias) for building `HistogramConfig` objects; exported from the top-level `plotez` namespace
- **New RTD examples**: `RTD_E13_histogram.py`, `RTD_E14_density.py`, `RTD_E15_errorband_relative.py` with corresponding PNG outputs in `examples/rtd_images/`
- **New README example**: `README_E7_histogram.py` + `README_E7_histogram.png` in `examples/ex_images/`
- **`docs/api.rst`**: Added `HistogramConfig` to "Parameter Classes"; added `histogram_config` to "Convenience / Wrapper Functions" with `hgc` row in alias table; added "Error band parameters" shorthand-key table (documents `ebc` aliases `c`, `ec`, `lw`, `ls`); added "Histogram parameters" shorthand-key table (documents `hgc` aliases `c`, `lw`, `ec`)
- **`docs/quickstart.rst`**: Added "Relative Error Band" section (E15), "Histogram" section (E13), and "Density Plot" section (E14); added `hgc` to "Shorthand Helpers" section

### Fixed

- **`docs/quickstart.rst`**: All 13 `.. literalinclude::` directives referenced `../examples/RTD_E*.py` but the scripts live in `../examples/rtd_images/`; corrected every path to include the `rtd_images/` subdirectory (this was a Sphinx build-breaking bug)
- **`docs/index.rst`**: Quick Example passed `auto_label=True` to `plot_xy`, which is not a parameter of that function; replaced with explicit `x_label=`, `y_label=`, and `data_label=` arguments
- **`src/plotez/plotez.py`**: `plot_two_column_file` docstring `Returns` section incorrectly stated `tuple[Axes, Axes] or Axes` (copy-pasted from `plot_with_dual_axes`); corrected to `Axes`

### Changed

- **`docs/index.rst`**: Features list updated — added "Histogram & Density Plotting" bullet; updated convenience wrappers bullet to include `hgc`; bumped coverage claim to 85%+
- **`README.md`**: Features list updated to match `index.rst`; added "### Histogram / Density" example section; bumped Project Status version to `v0.3.0` and coverage to `85%+`

## [v0.2.1] - 09-Mar-2026

### Added

- **Custom Exception Hierarchy**: Comprehensive domain-specific exceptions for better error handling
  - **Base exceptions**: `PlotError` (base for all plotting errors), `DataError` (data-related errors), `ConfigurationError` (config/parameter errors)
  - **Data exceptions**: `ShapeError` (invalid array shapes), `EmptyDataError` (empty required data), `ColumnCountError` (invalid file column count)
  - **Configuration exceptions**: `AxisLabelError` (wrong axis_labels length), `TwinXDataError` (invalid x2_data for dual-Y plots), `TwinYDataError` (invalid y2_data for dual-X plots)
  - **Custom warning**: `LabelConflictWarning` (for `auto_label` overriding user labels)
  - All exceptions available from `plotez.backend.error_handling` module
  - 19 new tests in `TestCustomExceptions` class for comprehensive exception coverage
- **Top-level wrapper aliases**: `lpc`, `epc`, `ebc`, `spc`, and their long-form equivalents (`line_plot_configuration`, `error_plot_configuration`, `error_band_configuration`, `scatter_plot_configuration`) are now exported from the top-level `plotez` namespace — no need to import from `plotez.backend` directly
- **Comprehensive wrapper function tests**: New `tests/test_wrappers.py` module with 34 tests covering:
  - All four wrapper functions (`lpc`, `epc`, `ebc`, `spc`) and their long-form equivalents
  - Parameter mapping from shorthand aliases to full parameter names
  - Edge cases (None values, zero values, sequences, extra kwargs)
  - Config object independence and integration scenarios
  - Achieves 100% coverage for `backend/_wrappers.py` module
- **`docs/api.rst`** — new "Convenience / Wrapper Functions" section with alias table and `autofunction` directives for all wrapper functions
- **`docs/api.rst`** — new "Shorthand Key Reference" section with RST tables documenting every accepted alias for line, error-bar, scatter, and figure parameters
- **`docs/quickstart.rst`** — new "Convenience / Wrapper Functions" section with before/after examples showing `epc()`, `lpc()`, `ebc()`, and `spc()`

### Changed

- **Code organization**: `src/plotez/plotez.py` reorganized with logical section headers for improved readability:
  - Error Visualization Functions (`plot_errorband`, `plot_errorbar`)
  - File I/O Functions (`plot_two_column_file`)
  - Simple Plotting Functions (`plot_xy`)
  - Dual-Axis Plotting Functions (`plot_xyy`, `plot_xxy`, `plot_with_dual_axes`)
  - Multi-Panel Plotting Functions (`two_subplots`, `n_plotter`)
- **Exception handling**: Replaced generic `ValueError` exceptions with specific custom exceptions
  - `plot_errorbar`: `ValueError` → `ShapeError` for invalid error array shapes
  - `plot_two_column_file`: `ValueError` → `ColumnCountError` for invalid file format
  - `dual_axes_data_validation`: `ValueError` → `AxisLabelError`, `EmptyDataError`, `TwinXDataError`, `TwinYDataError` for specific validation failures
  - `_auto_handler`: `UserWarning` → `LabelConflictWarning` for label override warnings
- **`docs/index.rst`** — Quick Example updated to use current API (`plot_errorbar` + `epc()`) instead of old `plot_errorbars` + `LinePlot` dict
- **`Project Status`** section replaced with a concise Markdown status table (version, Python support, coverage, docs link, license)
- **`docs/installation.rst`** — Requirements section corrected to list actual runtime deps (`matplotlib`, `numpy`)
  - Dev-dependency list replaced with a full table matching `requirements-dev.txt` (adds `black`, `isort`, `flake8`, `pydocstyle`, `pre-commit`, `sphinx-copybutton`, `myst-parser`, `build`)
- **`README.md`** — "Project Status" section replaced with a concise Markdown status table (version, Python support, coverage, docs link, license); Error Bar Plots example updated to use `epc()` with shorthand keyword aliases
- **Test coverage**: Overall project coverage increased to 91% (from ~85%), with `backend/_wrappers.py` achieving 100% coverage

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

## [v0.1.1] - 16-Feb-2026

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
- Type hints throughout the codebase (PEP 561 compliant with `py.typed` marker)
- Development tools integration:
    - pytest for testing
    - pytest-cov for coverage reporting
    - mypy for static type checking
    - Sphinx for documentation generation

### Notes

- First official release of plotez
- Evolved from the mpyez project with improved architecture and API
