import os
from typing import Literal
import requests
import base64
GITHUB_PAT_ENV_VAR = "GITHUB_PERSONAL_ACCESS_TOKEN"
def commit_character_to_file(username: str, repo: str, path: str, token: str, character: Literal['⬛', '⬜']):
    """Commit a single character to a file in a GitHub repo."""
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get the current file content
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content_data = response.json()
        content_sha = content_data['sha']
        current_content = base64.b64decode(content_data['content']).decode('utf-8').strip()
        new_content = current_content + character
        
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    data = {
        "message": "test updating message",
        "content": encoded_content,
        "sha": content_sha
    }

    update_response = requests.put(url, headers=headers, json=data)
    if update_response.status_code in [200, 201]:
        print("File updated successfully.")
    else:
        print("Failed to update the file.")

username = "glyn-stevens"
repo = "gitlab-scrolling-message"
path = "message.txt"
token = os.getenv(GITHUB_PAT_ENV_VAR)
if not token:
    raise ValueError(f"Expected environment variable {GITHUB_PAT_ENV_VAR}")
commit_character_to_file(username, repo, path, token, '⬛')
