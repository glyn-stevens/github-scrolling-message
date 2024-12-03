import numpy as np
from pathlib import Path
from lambda_func.constants import (
    ENCODED_MESSAGE_FILE,
    INPUT_MESSAGE_FILE,
    FULL_PIXELLATED_MESSAGE_FILE,
)
from lambda_func.convertors import pixel_array_to_string
from precalculation.char_to_pixel import CHAR_TO_PIXELS


def encode_and_save_message(
    input_msg: Path, test_output_file_path: Path, encoded_message_file_path: Path
):
    message = input_msg.read_text()
    pixel_array = encode_message_to_array(message, CHAR_TO_PIXELS)
    save_pixel_array_as_text(encoded_message_file_path, pixel_array)
    pixels_as_string = pixel_array_to_string(pixel_array.tolist(), pixel_array.size)
    test_output_file_path.write_text(pixels_as_string, encoding="utf-8")


def save_pixel_array_as_text(file_path: Path, pixel_array: np.ndarray) -> None:
    with open(file_path, "w") as f:
        for row in pixel_array:
            f.write("".join(map(str, row.astype(int))) + "\n")


def char_to_array(char: str, char_to_pixels: dict) -> np.ndarray:
    """Chararacter to numpy 6x7 array of 1s and 0s
    Character 5x5, with 2 rows padding below and 1 row padding to the right
    If char isn't in char_to_pixels then blank space is shown"""
    if char in char_to_pixels:
        pixel_matrix = np.array(
            [
                [0 if pixel == " " else 1 for pixel in row]
                for row in char_to_pixels[char]
            ]
        )
    else:
        pixel_matrix = np.zeros((5, 5))
    padding_bottom = np.vstack([np.zeros((1, 5)), np.ones((1, 5))])
    padding_right = np.vstack([np.zeros((6, 1)), np.ones((1, 1))])
    padded_pixel_matrix = np.hstack(
        [np.vstack([pixel_matrix, padding_bottom]), padding_right]
    )
    return padded_pixel_matrix


def encode_message_to_array(message: str, char_to_pixels: dict) -> np.ndarray:
    arrays = [char_to_array(char.upper(), char_to_pixels) for char in message]
    return np.hstack(arrays)


def main():
    print("🪄 Encoding message...")
    encode_and_save_message(
        INPUT_MESSAGE_FILE, FULL_PIXELLATED_MESSAGE_FILE, ENCODED_MESSAGE_FILE
    )


if __name__ == "__main__":
    main()
