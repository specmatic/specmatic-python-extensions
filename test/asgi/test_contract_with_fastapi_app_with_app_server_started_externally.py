import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.servers.asgi_app_server import ASGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FASTAPI_APP,
    FASTAPI_STR,
    PROJECT_ROOT,
)

app_server = ASGIAppServer(FASTAPI_STR, APP_HOST, APP_PORT)
app_server.start()


class TestContract:
    pass


(
    Specmatic(PROJECT_ROOT)
    .with_mock()
    .test_with_api_coverage_for_fastapi_app(TestContract, FASTAPI_APP)
    .run()
)

app_server.stop()

if __name__ == "__main__":
    pytest.main()
