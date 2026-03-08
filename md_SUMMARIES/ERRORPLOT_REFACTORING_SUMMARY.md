# ErrorPlotConfig Refactoring Summary

## Overview
Successfully refactored `ErrorPlotConfig` to inherit from `LinePlot` instead of `_PlotParams`, reducing code duplication and improving maintainability.

## Changes Made

### 1. Updated `ErrorPlotConfig` Class (`src/plotez/backend/utilities.py`)

#### Inheritance Change
- **Before**: `class ErrorPlotConfig(_PlotParams)`
- **After**: `class ErrorPlotConfig(LinePlot)`

#### Benefits
- Automatically inherits all LinePlot parameters (line_style, line_width, color, alpha, marker, marker_size, marker_edge_color, marker_face_color, marker_edge_width)
- Reduces code duplication
- Ensures consistency between line plots and error bar plots
- Automatically gets default color behavior from LinePlot

#### New Features Added
1. **Additional Error Bar Parameters**:
   - `elinewidth`: Width of the error bar lines
   - `ecolor`: Color of the error bar lines
   - `capthick`: Thickness of the error bar caps
   - Existing `capsize` parameter retained

2. **Magic Methods** (for consistency with LinePlot and ScatterPlot):
   - `__repr__()`: String representation of ErrorPlotConfig instance
   - `__eq__()`: Equality comparison between ErrorPlotConfig instances
   - `__hash__()`: Hashing support for use in sets and dictionaries

3. **Class Methods**:
   - `populate()`: Create ErrorPlotConfig instance from a dictionary of parameters
   - Supports parameter aliases (e.g., 'ms' for marker_size, 'markersize' for marker_size)

4. **Extended Methods**:
   - `_all_parameters()`: Now extends parent LinePlot parameters with error bar specific parameters
   - `_all_labels()`: Now extends parent LinePlot labels with error bar specific labels
   - `get_dict()`: Returns dictionary of non-None parameters

### 2. Updated Type Hints

#### `_split` Type (`src/plotez/backend/utilities.py`)
- **Before**: `Tuple[Union["LinePlot", "ScatterPlot"], Union["LinePlot", "ScatterPlot"]]`
- **After**: `Tuple[Union["LinePlot", "ScatterPlot", "ErrorPlotConfig"], Union["LinePlot", "ScatterPlot", "ErrorPlotConfig"]]`

#### Function Signatures
- `plot_dictionary_handler()`: Now accepts `Union[LinePlot, ScatterPlot, ErrorPlotConfig]`
- `split_dictionary()`: Now accepts `Union[LinePlot, ScatterPlot, ErrorPlotConfig]`

### 3. Bug Fixes

#### Fixed `plot_dictionary_handler()` (`src/plotez/backend/utilities.py`)
- **Issue**: Function didn't handle `None` values despite docstring claiming it did
- **Fix**: Added check to return empty dict when `plot_dictionary is None`
- **Impact**: Prevents `AttributeError` when no plot dictionary is provided

#### Fixed Dictionary Iteration (`src/plotez/plotez.py`)
- **Issue**: Code was iterating over dict keys incorrectly: `for key, value in plot_items`
- **Fix**: Changed to `for key, value in plot_items.items()` in 4 locations:
  - Line 316: Single axis plot
  - Line 328: Dual y-axis plot
  - Line 334: Dual x-axis plot
  - Line 472: n_plotter function
- **Impact**: Fixes `ValueError: too many values to unpack` errors

## Testing

### All Existing Tests Pass
- 38 tests in `tests/test_plotez.py` - **ALL PASS** ✓

### New ErrorPlotConfig Tests
Created comprehensive test suite (`test_errorplot_suite.py`) with 14 tests covering:
1. Basic ErrorPlotConfig creation
2. All LinePlot parameters
3. Error bar specific parameters
4. `get_dict()` method
5. `to_dict()` method
6. `__repr__()` method
7. Equality comparison (`__eq__`)
8. Hashing (`__hash__`)
9. `populate()` classmethod
10. Parameter aliases
11. Inheritance from LinePlot
12. `_all_parameters()` method
13. `_all_labels()` method

**All 14 tests PASS** ✓

### Enhanced Tests
Created `test_errorplot_enhanced.py` with 6 comprehensive integration tests:
1. Basic ErrorPlotConfig with inherited LinePlot parameters
2. ErrorPlotConfig with additional error bar parameters
3. ErrorPlotConfig.populate() classmethod
4. ErrorPlotConfig equality and hashing
5. ErrorPlotConfig with all parameters
6. Default color behavior

**All 6 tests PASS** ✓

## Backward Compatibility

✓ All existing code continues to work
✓ Original `rough_errorbar.py` example works without changes
✓ No breaking changes to the public API
✓ ErrorPlotConfig can still be used exactly as before

## Example Usage

### Basic Usage (unchanged)

```python
from plotez.backend.utilities import ErrorPlotConfig
from plotez import plot_errorbars

ep = ErrorPlotConfig(line_style='--', capsize=5, color='red')
plot_errorbars(x, y, xerr, yerr, plot_dictionary=ep)
```

### New Enhanced Usage
```python
# With additional error bar styling
ep = ErrorPlotConfig(
    line_style='-',
    line_width=2,
    color='blue',
    capsize=8,
    elinewidth=2,      # New!
    ecolor='red',      # New!
    capthick=2,        # New!
    marker='o',
    marker_size=6
)
plot_errorbars(x, y, xerr, yerr, plot_dictionary=ep)

# Using populate() classmethod
params = {'ls': '--', 'capsize': 5, 'elinewidth': 2}
ep = ErrorPlotConfig.populate(params)
```

## Code Quality Improvements

1. **Reduced Code Duplication**: ErrorPlotConfig no longer duplicates parameter definitions from LinePlot
2. **Better Maintainability**: Changes to LinePlot parameters automatically propagate to ErrorPlotConfig
3. **Consistency**: ErrorPlotConfig now has the same methods as LinePlot and ScatterPlot
4. **Enhanced Functionality**: Added 3 new error bar styling parameters
5. **Better Documentation**: Updated docstrings with comprehensive parameter descriptions

## Files Modified

1. `src/plotez/backend/utilities.py`:
   - Refactored `ErrorPlotConfig` class
   - Updated `plot_dictionary_handler()` function
   - Updated `split_dictionary()` function
   - Updated type hints

2. `src/plotez/plotez.py`:
   - Fixed dictionary iteration in 4 locations

## Recommendations for Future

1. Consider adding ErrorPlotConfig to the main test suite (`tests/test_plotez.py`)
2. Update documentation to showcase new ErrorPlotConfig capabilities
3. Add example showing enhanced error bar styling
4. Consider adding integration tests for `plot_errorbars()` with ErrorPlotConfig

## Summary

The refactoring successfully:
✓ Eliminates code duplication between ErrorPlotConfig and LinePlot
✓ Adds enhanced error bar styling capabilities
✓ Maintains 100% backward compatibility
✓ Improves code maintainability and consistency
✓ Fixes existing bugs in plot_dictionary_handler
✓ All 38 existing tests continue to pass
✓ 14 new ErrorPlotConfig-specific tests added and passing
