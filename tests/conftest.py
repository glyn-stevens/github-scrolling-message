from pathlib import Path
from pytest import fixture

TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / "data"


@fixture
def message_file() -> Path:
    return TEST_DATA_DIR / "test_file.txt"


@fixture
def repo_root_dir() -> Path:
    return TEST_DIR.parent
