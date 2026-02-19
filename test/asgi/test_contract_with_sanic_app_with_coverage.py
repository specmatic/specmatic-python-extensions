import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    PROJECT_ROOT,
    SANIC_APP,
    SANIC_STR,
)


class TestContract:
    pass


(
    Specmatic(PROJECT_ROOT)
    .with_mock()
    .with_asgi_app(SANIC_STR, APP_HOST, APP_PORT)
    .test_with_api_coverage_for_sanic_app(TestContract, SANIC_APP)
    .run()
)

if __name__ == "__main__":
    pytest.main()
