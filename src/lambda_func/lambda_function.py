from datetime import date
import os
from pathlib import Path

import numpy as np
from lambda_func.client import RepositoriesAPI

from lambda_func.constants import (
    GITHUB_PAT_ENV_VAR,
    GITHUB_REPO,
    GITHUB_USERNAME,
    MESSAGE_RECORD_FILE,
    START_DATE,
    ENCODED_MESSAGE_FILE,
)
from lambda_func.convertors import pixel_array_to_string


def lambda_handler(event, context) -> None:
    """Main entry point for lambda function"""
    message_pixel_array = np.load(ENCODED_MESSAGE_FILE)
    days_from_start = get_days_from_start(date.today, START_DATE)
    pixel_string_up_to_today = pixel_array_to_string(
        message_pixel_array, num_pixels_to_include=days_from_start + 1
    )
    if commit_on_day(message_pixel_array, days_from_start):
        repo_api = init_repo_api()
        commit_message_to_file(pixel_string_up_to_today, MESSAGE_RECORD_FILE, repo_api)


def get_days_from_start(day, start):
    return max((day - start).days, 0)


def commit_on_day(message_pixel_array: np.ndarray, idx: int) -> bool:
    row = idx % message_pixel_array.shape[0]
    col = idx // message_pixel_array.shape[0]
    try:
        return bool(message_pixel_array[row, col])
    except IndexError:
        return False


def init_repo_api() -> RepositoriesAPI:
    token = os.getenv(GITHUB_PAT_ENV_VAR)
    if not token:
        raise ValueError(f"Expected environment variable {GITHUB_PAT_ENV_VAR}")
    repo_api = RepositoriesAPI(GITHUB_USERNAME, GITHUB_REPO, token)
    return repo_api


def commit_message_to_file(
    message: str, file_path: Path, repo_api: RepositoriesAPI
) -> None:
    # Get the current file SHA (required to overwrite it)
    response = repo_api.get_file(file_path)
    current_content_sha = response.json()["sha"]

    repo_api.put_file(file_path, message, current_content_sha)
