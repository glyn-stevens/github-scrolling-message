from lambda_func.constants import MSG_EMPTY_PIXEL, MSG_FILLED_PIXEL


def pixel_array_to_string(
    pixel_array: list[list[int]],
    num_pixels_to_include: int,
    filled_pixel: str = MSG_FILLED_PIXEL,
    empty_pixel: str = MSG_EMPTY_PIXEL,
) -> str:
    if num_pixels_to_include < 1:
        return ""
    rows = len(pixel_array)
    cols = len(pixel_array[0])
    extra_cells = num_pixels_to_include % rows
    required_cols = num_pixels_to_include // rows + (extra_cells > 0)
    if required_cols > cols:
        required_cols = cols
        extra_cells = 0
    pixels_to_write = [row[:required_cols] for row in pixel_array]
    if extra_cells > 0:
        empty_padding = [None] * (rows - extra_cells)
        last_col = [pixels_to_write[i][-1] for i in range(extra_cells)] + empty_padding
        for i in range(rows):
            pixels_to_write[i] = pixels_to_write[i][: required_cols - 1] + [last_col[i]]
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
