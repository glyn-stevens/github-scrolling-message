from pathlib import Path
import requests  # type: ignore
import base64


class RepositoriesAPI:
    username: str
    repo: str
    token: str

    def __init__(self, username: str, repo: str, token: str):
        self.username = username
        self.repo = repo
        self.token = token

    def get_url(self, suffix: str) -> str:
        return f"https://api.github.com/repos/{self.username}/{self.repo}/{suffix.strip('/')}"

    def get_file_content(self, file_path: Path) -> requests.Response:
        """Response for API call to get file content from repo
        https://docs.github.com/en/rest/repos/contents"""
        url = self.get_url(f"/contents/{str(file_path)}")
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code != 200:
            raise ValueError(
                f"Expected response to either be OK or dealt with by method raise_for_status, got {response.status_code}"
            )
        return response

    def put_content_to_file(
        self,
        file_path: Path,
        new_content: str,
        current_content_sha: str,
        commit_message: str = "Commit made via API",
    ):
        """Put the provided content to the provided file, overwritting any existing content,
        and creating a commit to the repo
        https://docs.github.com/en/rest/repos/contents"""

        url = self.get_url(f"/contents/{str(file_path)}")
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        data = {
            "message": commit_message,
            "content": encoded_content,
            "sha": current_content_sha,
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValueError(
                f"Expected response to either be OK or dealt with by method raise_for_status, got {response.status_code}"
            )
        return response
