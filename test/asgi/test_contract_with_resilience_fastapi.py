import os
import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    ROOT_DIR,
    FASTAPI_APP,
    FASTAPI_STR,
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
)

os.environ["SPECMATIC_GENERATIVE_TESTS"] = "true"


class TestContract:
    pass


Specmatic().with_project_root(ROOT_DIR).with_mock(
    STUB_HOST, STUB_PORT, expectation_json_files
).with_asgi_app(FASTAPI_STR, APP_HOST, APP_PORT).test_with_api_coverage_for_fastapi_app(
    TestContract, FASTAPI_APP
).run()

os.environ["SPECMATIC_GENERATIVE_TESTS"] = "false"

if __name__ == "__main__":
    pytest.main()
