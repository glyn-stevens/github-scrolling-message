from pathlib import Path

import numpy as np
import pytest
from lambda_func.constants import MSG_EMPTY_PIXEL, MSG_FILLED_PIXEL
from lambda_func.convertors import pixel_array_to_string
from lambda_func.lambda_function import commit_on_day, load_pixel_array


def test_load_pixel_array(encoded_message_file: Path):
    expected = [
        [1, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ]
    loaded = load_pixel_array(encoded_message_file)
    assert loaded == expected


@pytest.mark.parametrize("days", [0, 1, 5, 7, 10, 20, 100, 1000])
def test_get_pixels_string_for_day(days: int, encoded_array: np.ndarray):
    pixel_string = pixel_array_to_string(encoded_array.tolist(), days + 1)
    assert len(pixel_string.splitlines()) == 7
    msg = (
        "Pixel string should have one char per day (inc. day 0), plus 7 new line chars"
    )
    assert len(pixel_string) == days + 1 + 7, msg
    assert all(c in [MSG_FILLED_PIXEL, MSG_EMPTY_PIXEL, "\n"] for c in pixel_string)


TEST_ARRAY = [[1, 0, 1], [1, 1, 0], [1, 0, 0]]


def test_commit_on_day():
    # Expected values when accessing by column-major index
    expected_values = [True, True, True, False, True, False, True, False, False]

    for idx, expected in enumerate(expected_values):
        msg = f"Expected {expected}, at index {idx}"
        assert commit_on_day(TEST_ARRAY, idx) == expected, msg


def test_commit_on_day_out_of_range():
    assert not commit_on_day(TEST_ARRAY, 9), "Expected False for out-of-range index"


def test_commit_on_day_negative():
    assert not commit_on_day(TEST_ARRAY, -5), "Expected False for negative index"
