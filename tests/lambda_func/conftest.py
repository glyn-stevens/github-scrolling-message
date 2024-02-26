from pytest import fixture

from lambda_func.client import RepositoriesAPI
from lambda_func.lambda_function import init_repo_api


@fixture
def repo_api() -> RepositoriesAPI:
    return init_repo_api()
