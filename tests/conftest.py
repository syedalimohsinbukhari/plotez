"""Pytest configuration and fixtures for plotez tests."""

import tempfile
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

# Use non-interactive backend for testing
matplotlib.use('Agg')


@pytest.fixture
def sample_x_data() -> np.ndarray:
    """Generate sample x data for testing."""
    return np.linspace(0, 10, 50)


@pytest.fixture
def sample_y_data() -> np.ndarray:
    """Generate sample y data for testing."""
    return np.sin(np.linspace(0, 10, 50))


@pytest.fixture
def sample_y2_data() -> np.ndarray:
    """Generate second sample y data for testing."""
    return np.cos(np.linspace(0, 10, 50))


@pytest.fixture
def sample_x_data_list() -> List[np.ndarray]:
    """Generate list of sample x data arrays for multi-plot testing."""
    return [
        np.linspace(0, 10, 50),
        np.linspace(0, 5, 30),
        np.linspace(0, 8, 40),
        np.linspace(0, 12, 60),
    ]


@pytest.fixture
def sample_y_data_list() -> List[np.ndarray]:
    """Generate list of sample y data arrays for multi-plot testing."""
    return [
        np.sin(np.linspace(0, 10, 50)),
        np.cos(np.linspace(0, 5, 30)),
        np.tan(np.linspace(0, 0.8, 40)),
        np.exp(np.linspace(0, 1, 60)),
    ]


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file with two columns."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("1.0,2.0\n")
        f.write("2.0,4.0\n")
        f.write("3.0,6.0\n")
        f.write("4.0,8.0\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    import os
    os.unlink(temp_path)


@pytest.fixture
def temp_csv_file_with_header():
    """Create a temporary CSV file with header."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("x,y\n")
        f.write("1.0,2.0\n")
        f.write("2.0,4.0\n")
        f.write("3.0,6.0\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    import os
    os.unlink(temp_path)


@pytest.fixture(autouse=True)
def cleanup_plots():
    """Automatically close all matplotlib figures after each test."""
    yield
    plt.close('all')

