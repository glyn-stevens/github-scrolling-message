from pathlib import Path
import numpy as np
from pytest import fixture

from lambda_func.client import RepositoriesAPI
from lambda_func.lambda_function import init_repo_api
from precalculation.char_to_pixel import CHAR_TO_PIXELS
from precalculation.encode import encode_message_to_array


@fixture
def repo_api() -> RepositoriesAPI:
    return init_repo_api()


@fixture
def encoded_array(message_file: Path) -> np.ndarray:
    return encode_message_to_array(message_file.read_text(), CHAR_TO_PIXELS)
