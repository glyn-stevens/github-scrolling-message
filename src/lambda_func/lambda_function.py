from datetime import date
import os
from pathlib import Path

from lambda_func.client import RepositoriesAPI

from lambda_func.constants import (
    GITHUB_PAT_ENV_VAR,
    GITHUB_REPO,
    GITHUB_USERNAME,
    RELATIVE_MESSAGE_RECORD_FILE,
    START_DATE,
    ENCODED_MESSAGE_FILE,
)
from lambda_func.convertors import pixel_array_to_string
import logging

logger = logging.getLogger()
if len(logger.handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logger.setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context) -> None:
    """Main entry point for lambda function"""
    logger.info("Running lambda handler...")
    message_pixel_array = load_pixel_array(ENCODED_MESSAGE_FILE)
    days_from_start = (date.today() - START_DATE).days
    logger.info(f"We've been running for {days_from_start} days.")
    if commit_on_day(message_pixel_array, days_from_start):
        logger.info("Filled in pixel required today. Committing to repo...")
        pixel_string_up_to_today = pixel_array_to_string(
            message_pixel_array, num_pixels_to_include=days_from_start + 1
        )
        repo_api = init_repo_api()
        try:
            commit_message_to_file(
                pixel_string_up_to_today, RELATIVE_MESSAGE_RECORD_FILE, repo_api
            )
            logger.info(f"Committed to repo {GITHUB_REPO}")
        except ValueError as e:
            logger.error(f"Failed to commit to repo. Error: {e}")
    else:
        logger.info("No commit necessary today")
    logger.info("Goodbye")


def load_pixel_array(file_path: Path) -> list[list[int]]:
    with open(file_path, "r") as f:
        return [[int(char) for char in line.strip()] for line in f.readlines()]


def get_days_from_start(day: date, start: date):
    return (day - start).days


def commit_on_day(message_pixel_array: list[list[int]], idx: int) -> bool:
    if idx < 0:
        return False
    rows = len(message_pixel_array)
    cols = len(message_pixel_array[0])
    row = idx % rows
    col = idx // rows
    if col >= cols:
        return False
    return bool(message_pixel_array[row][col])


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
    current_content_sha = response["sha"]
    repo_api.put_file(file_path, message, current_content_sha)
