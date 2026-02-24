"""Created on Feb 24 03:02:20 2026."""

LINE_ATTRS = {
    "ls": "line_style",
    "lw": "line_width",
    "color": "color",
    "alpha": "alpha",
    "marker": "marker",
    "ms": "marker_size",
    "mec": "marker_edge_color",
    "mfc": "marker_face_color",
    "mew": "marker_edge_width",
}

SCATTER_ATTRS = {"c": "color", "alpha": "alpha", "marker": "marker", "s": "size", "cmap": "cmap", "fc": "face_color"}

SUBPLOT_ATTRS = {"sharex": "share_x", "sharey": "share_y", "figsize": "fig_size"}

ERROR_ATTRS = {
    "elinewidth": "elinewidth",
    "ecolor": "ecolor",
    "capsize": "capsize",
    "capthick": "capthick",
} | LINE_ATTRS
