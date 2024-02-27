import numpy as np

from lambda_func.constants import MSG_EMPTY_PIXEL, MSG_FILLED_PIXEL


def pixel_array_to_string(
    pixel_array: np.ndarray,
    num_pixels_to_include: int,
    filled_pixel: str = MSG_FILLED_PIXEL,
    empty_pixel: str = MSG_EMPTY_PIXEL,
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
        empty_padding = np.empty((rows - extra_cells, 1))
        empty_padding[:] = None
        last_col = np.vstack(
            [
                pixels_to_write[:extra_cells, -1].reshape(-1, 1),
                empty_padding,
            ]
        )
        pixels_to_write = np.hstack([pixels_to_write[:, : requied_cols - 1], last_col])
    string_pixels = ""

    def pixel_from_value(val: int | None) -> str:
        match val:
            case 0:
                return empty_pixel
            case 1:
                return filled_pixel
            case _:
                return ""

    for row in pixels_to_write:
        string_pixels += "".join(pixel_from_value(val) for val in row) + "\n"
    return string_pixels
