import base64
from pathlib import Path
from lambda_func.client import RepositoriesAPI


def test_get_file(repo_api: RepositoriesAPI, test_message_file: Path, repo_root_dir: Path):
    expected_msg = test_message_file.read_text()
        
    response = repo_api.get_file(test_message_file.relative_to(repo_root_dir))
    
    assert response.status_code == 200
    decoded_content = base64.b64decode(response.json()["content"]).decode('utf-8')
    assert decoded_content == expected_msg
