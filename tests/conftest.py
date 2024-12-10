from pathlib import Path
from pytest import fixture

from tests import TEST_DIR, TEST_DATA_DIR


@fixture
def message_file() -> Path:
    return TEST_DATA_DIR / "test_file.txt"


@fixture
def repo_root_dir() -> Path:
    return TEST_DIR.parent
