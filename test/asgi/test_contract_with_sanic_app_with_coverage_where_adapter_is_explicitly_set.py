import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.coverage.sanic_app_route_adapter import SanicAppRouteAdapter
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
    .test_with_api_coverage(TestContract, SanicAppRouteAdapter(SANIC_APP))
    .run()
)

if __name__ == "__main__":
    pytest.main()
