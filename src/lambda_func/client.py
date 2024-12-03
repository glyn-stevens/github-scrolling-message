from pathlib import Path
import urllib3
import json
import base64


class RepositoriesAPI:
    username: str
    repo: str
    token: str

    def __init__(self, username: str, repo: str, token: str):
        self.username = username
        self.repo = repo
        self.token = token
        self.http = urllib3.PoolManager()

    def _get_url(self, suffix: str) -> str:
        return f"https://api.github.com/repos/{self.username}/{self.repo}/{suffix.strip('/')}"

    def get_file(self, file_path: Path) -> dict:
        """Response for API call to get file content from repo
        https://docs.github.com/en/rest/repos/contents"""
        url = self._get_url(f"/contents/{file_path.as_posix()}")
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = self.http.request("GET", url, headers=headers)

        if response.status != 200:
            raise ValueError(
                f"Expected 200 OK, got {response.status} with body {response.data.decode()}"
            )

        return json.loads(response.data.decode())

    def put_file(
        self,
        file_path: Path,
        new_content: str,
        current_content_sha: str,
        commit_message: str = "Commit made via API",
    ):
        """Put the provided content to the provided file, overwritting any existing content,
        and creating a commit to the repo
        https://docs.github.com/en/rest/repos/contents"""

        url = self._get_url(f"/contents/{file_path.as_posix()}")
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        data = {
            "message": commit_message,
            "content": encoded_content,
            "sha": current_content_sha,
        }

        response = self.http.request(
            "PUT", url, headers=headers, body=json.dumps(data).encode("utf-8")
        )

        if response.status != 200:
            raise ValueError(
                f"Expected 200 OK, got {response.status} with body {response.data.decode()}"
            )

        return json.loads(response.data.decode())
