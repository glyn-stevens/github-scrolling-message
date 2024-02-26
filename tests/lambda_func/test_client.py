import base64
from pathlib import Path
from lambda_func.client import RepositoriesAPI


def test_get_file(
    repo_api: RepositoriesAPI, test_message_file: Path, repo_root_dir: Path
):
    expected_msg = test_message_file.read_text()

    response = repo_api.get_file(test_message_file.relative_to(repo_root_dir))

    assert response.status_code == 200
    decoded_content = decode_content(response)
    assert decoded_content == expected_msg


def decode_content(response):
    return base64.b64decode(response.json()["content"]).decode("utf-8")


def test_put_file(
    repo_api: RepositoriesAPI, test_message_file: Path, repo_root_dir: Path
):
    file_rel_path = test_message_file.relative_to(repo_root_dir)
    get_file_response = repo_api.get_file(file_rel_path)
    current_sha = get_file_response.json()["sha"]
    original_msg = decode_content(get_file_response)
    new_msg = "New message to put to file"
    assert original_msg != new_msg, "Test should be trying to change the file content?"

    # Put the new message to the file
    put_response = repo_api.put_file(
        file_rel_path,
        new_content=new_msg,
        current_content_sha=current_sha,
        commit_message="Test put file via API - set to new message",
    )
    try:
        assert put_response.status_code == 200
        new_get_file_response = repo_api.get_file(file_rel_path)
        assert (
            decode_content(new_get_file_response) == new_msg
        ), "New message not put correctly?"
    finally:
        new_sha = new_get_file_response.json()["sha"]
        repo_api.put_file(
            file_rel_path,
            new_content=original_msg,
            current_content_sha=new_sha,
            commit_message="Test put file via API - reset",
        )
