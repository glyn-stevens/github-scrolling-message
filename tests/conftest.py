from pathlib import Path
from pytest import fixture

TEST_DATA_DIR = Path(__file__).parent / "data"


@fixture
def test_message_file() -> Path:
    return TEST_DATA_DIR / "test_file.txt"
