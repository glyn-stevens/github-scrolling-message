from datetime import date
import os
from pathlib import Path
from lambda_func.client import RepositoriesAPI

from lambda_func.constants import (
    GITHUB_PAT_ENV_VAR,
    GITHUB_REPO,
    GITHUB_USERNAME,
    MESSAGE_RECORD_FILE,
    MSG_FILLED_PIXEL,
    START_DATE,
)
from lambda_func.convertors import pixel_array_to_string


def lambda_handler(event, context) -> None:
    """Main entry point for lambda function"""
    message_pixel_array = read_message()
    days_from_start = (date.today() - START_DATE).days
    pixel_string_up_to_today = pixel_array_to_string(
        message_pixel_array, num_pixels_to_include=days_from_start
    )
    if pixel_string_up_to_today[-1] == MSG_FILLED_PIXEL:
        # Pixel for today is dark, so we need to commit to file
        repo_api = init_repo_api()
        commit_message_to_file(pixel_string_up_to_today, MESSAGE_RECORD_FILE, repo_api)


def init_repo_api():
    token = os.getenv(GITHUB_PAT_ENV_VAR)
    if not token:
        raise ValueError(f"Expected environment variable {GITHUB_PAT_ENV_VAR}")
    repo_api = RepositoriesAPI(GITHUB_USERNAME, GITHUB_REPO, token)
    return repo_api


def commit_message_to_file(
    message: str, file_path: Path, repo_api: RepositoriesAPI
) -> None:
    # Get the current file SHA (required to overwrite it)
    response = repo_api.get_file_content(file_path)
    current_content_sha = response.json()["sha"]

    repo_api.put_content_to_file(file_path, message, current_content_sha)
