import os
import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    ROOT_DIR,
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
)
from test.config import SPECMATIC_CONFIG_CUSTOM


class TestContract:
    pass


os.environ["SPECMATIC_GENERATIVE_TESTS"] = "true"

Specmatic().with_project_root(ROOT_DIR).with_specmatic_config_file_path(SPECMATIC_CONFIG_CUSTOM).with_mock(
    STUB_HOST, STUB_PORT, expectation_json_files
).with_wsgi_app(
    FLASK_APP,
    APP_HOST,
    APP_PORT,
).test_with_api_coverage_for_flask_app(TestContract, FLASK_APP).run()


os.environ["SPECMATIC_GENERATIVE_TESTS"] = "false"

if __name__ == "__main__":
    pytest.main()
