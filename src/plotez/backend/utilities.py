"""
PlotEZ Backend Utilities.

Utility classes and functions for plot parameter management and data validation.
"""

from __future__ import annotations

import warnings

__all__ = [
    "dual_axes_data_validation",
    "error_band_validation",
    "error_offset_validation",
    "errorbar_validation",
    "plot_or_scatter",
    "validate_1d",
    "validate_equal_length",
]

import numpy as np

from ..errors import (
    AxisLabelError,
    ConfigurationError,
    DataLengthError,
    EmptyDataError,
    ShapeError,
    TwinXDataError,
    TwinYDataError,
)
from ..typing import ArrayLike, Axes, NDArray


def dual_axes_data_validation(
    x1_data: ArrayLike,
    x2_data: ArrayLike | None,
    y1_data: ArrayLike,
    y2_data: ArrayLike | None,
    use_twin_x: bool,
    axis_labels: list[str | None],
) -> tuple[NDArray, NDArray, NDArray | None, NDArray | None]:
    """
    Validate the data and parameters for dual-axes plotting.

    Parameters
    ----------
    x1_data :
        Data for the primary x-axis.
    x2_data :
        Data for the secondary x-axis (used in dual x-axis plots). Should be `None` if `use_twin_x` is True.
    y1_data :
        Data for the primary y-axis.
    y2_data :
        Data for the secondary y-axis (used in dual y-axis plots). Should be `None` if `use_twin_x` is False.
    use_twin_x :
        If True, a dual y-axis plot is expected; otherwise, a dual x-axis plot is expected.
    axis_labels :
        List of axis labels. Must have exactly three elements:
        - Label for the x-axis of the primary plot.
        - Label for the y-axis of the primary plot.
        - Label for the secondary axis (x or y).

    Raises
    ------
    AxisLabelError
        If ``axis_labels`` does not have exactly three elements.
    EmptyDataError
        If ``x1_data`` or ``y1_data`` is empty.
    TwinXDataError
        If ``x2_data`` is provided when ``use_twin_x`` is ``True``.
    TwinYDataError
        If ``y2_data`` is provided when ``use_twin_x`` is ``False``.
    """
    if isinstance(axis_labels, str):
        raise AxisLabelError(
            f"axis_labels must be a list of 3 strings, not a plain string. Did you mean ['{axis_labels}']?"
        )

    x1_data, y1_data = np.asarray(x1_data), np.asarray(y1_data)
    validate_1d(x1_data, y1_data, names=["x1_data", "y1_data"])
    if len(x1_data) == 0 or len(y1_data) == 0:
        raise EmptyDataError("Primary x or y data is empty. Please provide valid data.")
    validate_equal_length(x1_data, y1_data, names=["x1_data", "y1_data"])

    if x2_data is not None:
        x2_data = np.asarray(x2_data)
        validate_1d(x2_data, names=["x2_data"])

    if y2_data is not None:
        y2_data = np.asarray(y2_data)
        validate_1d(y2_data, names=["y2_data"])

    if len(axis_labels) != 3:  # noqa
        raise AxisLabelError("The axis_labels should have a length of 3.")
    if use_twin_x and x2_data is not None:
        raise TwinXDataError("Dual Y-axis plot requested but 'x2_data' given.")
    if not use_twin_x and y2_data is not None:
        raise TwinYDataError("Dual X-axis plot requested but 'y2_data' given.")
    if use_twin_x and y2_data is not None:
        validate_equal_length(x1_data, y2_data, names=["x1_data", "y2_data"])
    if not use_twin_x and x2_data is not None:
        validate_equal_length(x2_data, y1_data, names=["x2_data", "y1_data"])

    return x1_data, y1_data, x2_data, y2_data


def plot_or_scatter(axis: Axes | None = None, scatter: bool = False, axes: Axes | None = None):
    """
    Return the plot or scatter method based on the specified plot type.

    Parameters
    ----------
    axis :
        The matplotlib axis on which to apply the plot or scatter method.
    scatter :
        If True, returns the scatter method; otherwise, returns the plot method.
    axes :
        .. deprecated:: v0.3.4
            Use ``axis`` instead. This parameter will be removed in a future version.

    Returns
    -------
    function
        The matplotlib plotting method (``axis.scatter`` if ``scatter`` is True, otherwise ``axis.plot``).
    """
    if axis is None and axes is None:
        raise ValueError("Either 'axis' or 'axes' must be provided.")

    if axes is not None:
        warnings.warn(
            "Parameter 'axes' is deprecated and will be removed in a future version. " "Use 'axis' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        axis = axes

    if not isinstance(axis, Axes):
        raise TypeError(f"'axis' must be a matplotlib Axes object, got {type(axis).__name__!r}.")

    return axis.scatter if scatter else axis.plot


def validate_1d(*arrays: NDArray, names: list[str]) -> None:
    """Verify that every supplied array is exactly 1-D.

    Parameters
    ----------
    *arrays :
        Arrays to check (already converted with ``np.asarray``).
    names :
        Human-readable name for each array, used in the error message.

    Raises
    ------
    ShapeError
        If any array has `ndim != 1`.
    """
    for arr, name in zip(arrays, names):
        if arr.ndim != 1:
            raise ShapeError(f"'{name}' must be 1D, got shape {arr.shape}")


def validate_equal_length(*arrays: NDArray, names: list[str]) -> None:
    """Verify that all supplied arrays share the same length.

    Scalar (0-d) arrays are skipped — they broadcast freely and do not need a length check.

    Parameters
    ----------
    *arrays :
        Arrays to check (already converted with `np.asarray`).
    names :
        Human-readable name for each array, used in the error message.

    Raises
    ------
    DataLengthError
        If the arrays do not all have the same length.
    """
    checkable = [(arr, name) for arr, name in zip(arrays, names) if arr.ndim >= 1]
    if not checkable:
        return
    lengths = [len(arr) for arr, _ in checkable]
    if len(set(lengths)) > 1:
        parts = ", ".join(f"'{n}'={length}" for (_, n), length in zip(checkable, lengths))
        raise DataLengthError(f"Arrays must have equal length, got: {parts}")


def errorbar_validation(
    x: NDArray, y: NDArray, x_err: ArrayLike | None, y_err: ArrayLike | None
) -> tuple[NDArray | None, NDArray | None]:
    """Validate the input arrays for error bars to ensure compatibility with the provided data arrays.

    Parameters
    ----------
    x :
        The array of x-coordinate data.
    y :
        The array of y-coordinate data.
    x_err :
        The error values associated with the x-coordinate data.
        Can represent either symmetric or asymmetric errors.

        - If symmetric, it should be a 1D array.
        - If asymmetric, it should be a 2D array with shape (2, N).
        - Can also be `None`, in which case no validation is performed for x-error.
    y_err :
        The error values associated with the y-coordinate data.
        Can represent either symmetric or asymmetric errors.

        - If symmetric, it should be a 1D array.
        - If asymmetric, it should be a 2D array with shape (2, N).
        - Can also be `None`, in which case no validation is performed for y-error.

    Returns
    -------
    tuple[NDArray | None, NDArray | None]
        A tuple containing the validated `x_err` and `y_err` arrays, respectively.
        If no validation is performed for a specific error array (i.e., it is `None`), it is returned as `None`.

    Raises
    ------
    ShapeError
        Raised if the shape of `x_err` or `y_err` does not conform to valid symmetric or asymmetric error formats.
    DataLengthError
        Raised if the length of the `x_err` or `y_err` array does not match the length of `x` or `y` data array.
    """
    if x_err is not None:
        x_err: NDArray = np.asarray(x_err)
        if x_err.ndim > 2 or (x_err.ndim == 2 and x_err.shape[0] != 2):
            raise ShapeError(f"Asymmetric `x_err` must have shape (2, N), got {x_err.shape}")
        if x_err.ndim == 1:
            validate_equal_length(x, x_err, names=["x_data", "x_err"])
        elif x_err.ndim == 2 and x_err.shape[1] != len(x):
            raise DataLengthError(f"'x_err' must have length {len(x)} along axis 1, got {x_err.shape[1]}")

    if y_err is not None:
        y_err: NDArray = np.asarray(y_err)
        if y_err.ndim > 2 or (y_err.ndim == 2 and y_err.shape[0] != 2):
            raise ShapeError(f"Asymmetric `y_err` must have shape (2, N), got {y_err.shape}")
        if y_err.ndim == 1:
            validate_equal_length(y, y_err, names=["y_data", "y_err"])
        elif y_err.ndim == 2 and y_err.shape[1] != len(y):
            raise DataLengthError(f"'y_err' must have length {len(y)} along axis 1, got {y_err.shape[1]}")

    return x_err, y_err


def error_band_validation(
    x: NDArray, y: NDArray, y_lower: ArrayLike | None, y_upper: ArrayLike | None
) -> tuple[NDArray | None, NDArray | None]:
    """Validate the input parameters for an error band visualization process.

    Parameters
    ----------
    x :
        Primary data on the x-axis to be validated.
    y :
        Primary data on the y-axis to be validated.
    y_lower :
        Optional lower-bound data for the error band, validated if provided.
    y_upper :
        Optional upper-bound data for the error band, validated if provided.

    Returns
    -------
    tuple[NDArray | None, NDArray | None]
        A tuple containing the validated `x_err` and `y_err` arrays, respectively.
        If no validation is performed for a specific error array (i.e., it is `None`), it is returned as `None`.
    """
    if y_lower is None and y_upper is None:
        raise ConfigurationError("At least one of `y_lower` or `y_upper` must be provided for the error band.")

    if y_lower is not None:
        y_lower = np.asarray(y_lower)
        if y_lower.ndim > 0:
            validate_1d(y_lower, names=["y_lower"])
    if y_upper is not None:
        y_upper = np.asarray(y_upper)
        if y_upper.ndim > 0:
            validate_1d(y_upper, names=["y_upper"])

    supplied_bounds = [array for array in (y_lower, y_upper) if array is not None]
    supplied_names = [name for array, name in ((y_lower, "y_lower"), (y_upper, "y_upper")) if array is not None]
    validate_equal_length(x, y, *supplied_bounds, names=["x_data", "y_data", *supplied_names])

    return y_lower, y_upper


def error_offset_validation(
    y: NDArray, y_lower: ArrayLike | None, y_upper: ArrayLike | None
) -> tuple[NDArray | None, NDArray | None]:
    """Validate and processes the lower and upper error offset arrays relative to a target array.

    Parameters
    ----------
    y :
        The target array against which the error offsets are validated.
    y_lower :
        The lower error offsets.
        Can be None.
        If provided, it is validated for dimensionality and length.
    y_upper :
        The upper error offsets.
        Can be None.
        If provided, it is validated for dimensionality and length.

    Returns
    -------
    tuple[NDArray | None, NDArray | None]
        A tuple containing the validated `x_lower` and `y_lower` arrays, respectively.
        If no validation is performed for a specific error array (i.e., it is `None`), it is returned as `None`.
    """
    lower_offset = np.asarray(y_lower) if y_lower is not None else None
    upper_offset = np.asarray(y_upper) if y_upper is not None else None

    if lower_offset is not None and lower_offset.ndim > 0:
        validate_1d(lower_offset, names=["y_lower"])
        validate_equal_length(y, lower_offset, names=["y_data", "y_lower"])

    if upper_offset is not None and upper_offset.ndim > 0:
        validate_1d(upper_offset, names=["y_upper"])
        validate_equal_length(y, upper_offset, names=["y_data", "y_upper"])

    return lower_offset, upper_offset
