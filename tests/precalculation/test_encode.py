from precalculation.char_to_pixel import CHAR_TO_PIXELS
from precalculation.encode import encode_message_to_array


def test_encode_message():
    test_message = "My test message!?@{}"
    encoded_array = encode_message_to_array(test_message, CHAR_TO_PIXELS)
    assert encoded_array.shape[0] == 7
    assert encoded_array.shape[1] == 6 * len(test_message)
    
