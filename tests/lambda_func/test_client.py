import base64
from pathlib import Path
from lambda_func.client import RepositoriesAPI


def test_get_file(repo_api: RepositoriesAPI, message_file: Path, repo_root_dir: Path):
    expected_msg = message_file.read_text()

    response = repo_api.get_file(message_file.relative_to(repo_root_dir))

    assert "content" in response, "Response missing 'content' key"
    decoded_content = decode_content(response["content"])
    assert decoded_content == expected_msg


def decode_content(encoded_content: str) -> str:
    return base64.b64decode(encoded_content).decode("utf-8")


def test_put_file(repo_api: RepositoriesAPI, message_file: Path, repo_root_dir: Path):
    file_rel_path = message_file.relative_to(repo_root_dir)
    get_file_response = repo_api.get_file(file_rel_path)
    current_sha = get_file_response["sha"]
    original_msg = decode_content(get_file_response["content"])
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
        assert "commit" in put_response, "Response missing 'commit' key"
        new_get_file_response = repo_api.get_file(file_rel_path)
        assert (
            decode_content(new_get_file_response["content"]) == new_msg
        ), "New message not put correctly?"
    finally:
        new_sha = new_get_file_response["sha"]
        repo_api.put_file(
            file_rel_path,
            new_content=original_msg,
            current_content_sha=new_sha,
            commit_message="Test put file via API - reset",
        )
