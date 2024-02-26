from precalculation.char_to_pixel import CHAR_TO_PIXELS
from precalculation.encode import encode_message_to_array

TEST_MESSAGE = "My test message!?@{}"


def test_encode_message():
    encoded_array = encode_message_to_array(TEST_MESSAGE, CHAR_TO_PIXELS)
    assert encoded_array.shape[0] == 7, "Expected pixel grid to be 7 px height"
    msg = "Expected pixel grid to have 6 px (5 for letter + 1 padding) of width per letter"
    assert encoded_array.shape[1] == 6 * len(TEST_MESSAGE), msg
