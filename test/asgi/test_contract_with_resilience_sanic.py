import os
import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    ROOT_DIR,
    SANIC_APP,
    SANIC_STR,
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
)

os.environ["SPECMATIC_GENERATIVE_TESTS"] = "true"


class TestContract:
    pass


Specmatic().with_project_root(ROOT_DIR).with_mock(
    MOCK_HOST, MOCK_PORT, expectation_json_files
).with_asgi_app(SANIC_STR, APP_HOST, APP_PORT).test_with_api_coverage_for_sanic_app(
    TestContract, SANIC_APP
).run()

os.environ["SPECMATIC_GENERATIVE_TESTS"] = "false"

if __name__ == "__main__":
    pytest.main()
