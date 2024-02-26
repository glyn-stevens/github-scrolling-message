import numpy as np

from lambda_func.constants import MSG_EMPTY_PIXEL, MSG_FILLED_PIXEL


def pixel_array_to_string(
    pixel_array: np.ndarray,
    num_pixels_to_include: int,
    filled_pixel: str = MSG_FILLED_PIXEL,
    exmpty_pixel: str = MSG_EMPTY_PIXEL,
) -> str:
    if num_pixels_to_include < 1:
        return ""
    rows, cols = pixel_array.shape
    extra_cells = num_pixels_to_include % rows
    requied_cols = num_pixels_to_include // rows + (extra_cells > 0)
    if requied_cols > cols:
        requied_cols = cols
        extra_cells = 0
    pixels_to_write = pixel_array[:, :requied_cols]
    if extra_cells > 0:
        last_col = np.vstack(
            [
                pixels_to_write[:extra_cells, -1].reshape(-1, 1),
                np.zeros((rows - extra_cells, 1)),
            ]
        )
        pixels_to_write = np.hstack([pixels_to_write[:, : requied_cols - 1], last_col])
    string_pixels = ""
    for row in pixels_to_write:
        string_pixels += (
            "".join(filled_pixel if x else exmpty_pixel for x in row) + "\n"
        )
    return string_pixels
