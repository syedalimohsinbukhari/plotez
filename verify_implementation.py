#!/usr/bin/env python3
"""Verification script for PlotEZ implementation."""

import sys
import os

# Add src to path for verification
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all main functions can be imported."""
    print("Testing imports...")
    try:
        from plotez import (
            plot_two_column_file,
            plot_xy,
            plot_xyy,
            plot_with_dual_axes,
            two_subplots,
            n_plotter,
            __version__
        )
        print(f"✓ All imports successful")
        print(f"✓ PlotEZ version: {__version__}")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_backend_imports():
    """Test that backend modules can be imported."""
    print("\nTesting backend imports...")
    try:
        from plotez.backend.utilities import LinePlot, ScatterPlot, SubPlots
        from plotez.backend.error_handling import PlotError, NoXYLabels, OrientationError
        print(f"✓ Backend utilities imported")
        print(f"✓ Error handling imported")
        return True
    except ImportError as e:
        print(f"✗ Backend import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic plotting functionality."""
    print("\nTesting basic functionality...")
    try:
        import numpy as np
        from plotez import plot_xy

        x = np.linspace(0, 10, 50)
        y = np.sin(x)

        # This should not raise an error
        result = plot_xy(x, y, auto_label=True)
        print(f"✓ Basic plot_xy works")
        return True
    except Exception as e:
        print(f"✗ Basic functionality failed: {e}")
        return False

def check_files():
    """Check that all expected files exist."""
    print("\nChecking file structure...")
    expected_files = [
        'src/plotez/__init__.py',
        'src/plotez/plotez.py',
        'src/plotez/py.typed',
        'src/plotez/version.py',
        'src/plotez/backend/utilities.py',
        'src/plotez/backend/error_handling.py',
        'tests/test_plotez.py',
        'tests/test_utilities.py',
        'tests/test_error_handling.py',
        'tests/conftest.py',
        'docs/conf.py',
        'docs/index.rst',
        'docs/CHANGELOG.md',
        'pyproject.toml',
        'README.md',
    ]

    all_exist = True
    for filepath in expected_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - MISSING")
            all_exist = False

    return all_exist

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("PlotEZ Implementation Verification")
    print("=" * 60)

    results = []

    results.append(("File Structure", check_files()))
    results.append(("Main Imports", test_imports()))
    results.append(("Backend Imports", test_backend_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")

    all_passed = all(result[1] for result in results)

    print("=" * 60)
    if all_passed:
        print("✓ All verification checks PASSED!")
    else:
        print("✗ Some verification checks FAILED")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

