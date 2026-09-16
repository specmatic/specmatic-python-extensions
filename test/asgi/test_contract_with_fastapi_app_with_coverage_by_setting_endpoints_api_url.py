import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.coverage.servers.fastapi_app_coverage_server import (
    FastApiAppCoverageServer,
)
from specmatic.servers.asgi_app_server import ASGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FASTAPI_APP,
    FASTAPI_STR,
    PROJECT_ROOT,
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
)

app_server = ASGIAppServer(FASTAPI_STR, APP_HOST, APP_PORT)
coverage_server = FastApiAppCoverageServer(FASTAPI_APP)


class TestContract:
    pass


app_server.start()
try:
    coverage_server.start()
    try:
        (
            Specmatic(PROJECT_ROOT)
            .with_mock()
            .with_endpoints_api(coverage_server.endpoints_api)
            .test(TestContract)
            .run()
        )
    finally:
        coverage_server.stop()
finally:
    app_server.stop()

if __name__ == "__main__":
    pytest.main()
