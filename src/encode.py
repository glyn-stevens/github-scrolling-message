import numpy as np
from pathlib import Path
from char_to_pixel import CHAR_TO_PIXELS
from datetime import date

START_DATE = date(2024, 1, 12)
DATA_DIR = Path.cwd() / "data"
MESSAGE_FILE = DATA_DIR / "message_to_print.txt"


def main():
    message = get_message(MESSAGE_FILE)
    pixel_array = message_to_pixels(message, CHAR_TO_PIXELS)
    # days_from_start = (date.today() - START_DATE).days
    days_from_start = 10000
    write_message(pixel_array, days_from_start)


def write_message(
    pixel_array: np.ndarray,
    days: int,
    filled_pixel: str = "⬛",
    exmpty_pixel: str = "⬜",
):
    if days < 1:
        return
    rows, cols = pixel_array.shape
    extra_cells = days % rows
    requied_cols = days // rows + (extra_cells > 0)
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

    with open(Path("message.txt"), "w", encoding="utf-8") as f:
        for row in pixels_to_write:
            line = "".join(filled_pixel if x else exmpty_pixel for x in row) + "\n"
            f.write(line)


def get_message(file_path: Path):
    with open(file_path, "r") as f:
        message = f.read()
    return message


def char_to_array(char: str, char_to_pixels: dict) -> np.ndarray:
    if char in char_to_pixels:
        pixel_matrix = np.array(
            [
                [0 if pixel == " " else 1 for pixel in row]
                for row in char_to_pixels[char]
            ]
        )
        pixel_matrix = np.vstack([pixel_matrix, np.zeros((1, 5)), np.ones((1, 5))])
    else:
        pixel_matrix = np.vstack([np.zeros((6, 5)), np.ones((1, 5))])

    pixel_matrix = np.hstack([pixel_matrix, np.zeros((7, 1))])
    return pixel_matrix


def message_to_pixels(message: str, char_to_pixels: dict) -> np.ndarray:
    arrays = [char_to_array(char.upper(), char_to_pixels) for char in message]
    full_array = np.hstack(arrays)
    return full_array


main()
