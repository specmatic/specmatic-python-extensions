import os

import pytest

from specmatic.core.specmatic import Specmatic
from test import ROOT_DIR, SANIC_STR, MOCK_HOST, MOCK_PORT, expectation_json_files


class TestContract:
    pass


def set_app_config(host: str, port: int):
    os.environ["ORDER_API_HOST"] = host
    os.environ["ORDER_API_PORT"] = str(port)
    os.environ["API_URL"] = f"http://{host}:{port}"


def reset_app_config():
    os.environ["ORDER_API_HOST"] = MOCK_HOST
    os.environ["ORDER_API_PORT"] = str(MOCK_PORT)
    os.environ["API_URL"] = f"http://{MOCK_HOST}:{MOCK_PORT}"


Specmatic().with_project_root(ROOT_DIR).with_mock(
    expectations=expectation_json_files
).with_asgi_app(
    SANIC_STR,
    set_app_config_func=set_app_config,
    reset_app_config_func=reset_app_config,
).test(TestContract).run()

if __name__ == "__main__":
    pytest.main()
