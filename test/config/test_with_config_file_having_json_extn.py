import os

import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    PROJECT_ROOT,
)
from test.config import SPECMATIC_CONFIG_YAML


class TestContract:
    pass


os.rename(SPECMATIC_CONFIG_YAML, SPECMATIC_CONFIG_YAML + ".bak")

(
    Specmatic(PROJECT_ROOT)
    .with_mock()
    .with_wsgi_app(FLASK_APP, APP_HOST, APP_PORT)
    .test_with_api_coverage_for_flask_app(TestContract, FLASK_APP)
    .run()
)


os.rename(SPECMATIC_CONFIG_YAML + ".bak", SPECMATIC_CONFIG_YAML)

if __name__ == "__main__":
    pytest.main()