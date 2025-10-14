import os
import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    ROOT_DIR,
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
)
from test.config import SPECMATIC_CONFIG_JSON


class TestContract:
    pass


os.environ["SPECMATIC_GENERATIVE_TESTS"] = "true"
os.rename(SPECMATIC_CONFIG_JSON, SPECMATIC_CONFIG_JSON + ".bak")

Specmatic().with_project_root(ROOT_DIR).with_mock(
    MOCK_HOST, MOCK_PORT, expectation_json_files
).with_wsgi_app(
    FLASK_APP,
    APP_HOST,
    APP_PORT,
).test_with_api_coverage_for_flask_app(TestContract, FLASK_APP).run()


os.environ["SPECMATIC_GENERATIVE_TESTS"] = "false"
os.rename(SPECMATIC_CONFIG_JSON + ".bak", SPECMATIC_CONFIG_JSON)

if __name__ == "__main__":
    pytest.main()
