import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.servers.asgi_app_server import ASGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FASTAPI_APP,
    FASTAPI_STR,
    ROOT_DIR,
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
)

app_server = ASGIAppServer(FASTAPI_STR, APP_HOST, APP_PORT)
app_server.start()


class TestContract:
    pass


Specmatic().with_project_root(ROOT_DIR).with_mock(
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
).test_with_api_coverage_for_fastapi_app(
    TestContract, FASTAPI_APP, APP_HOST, APP_PORT
).run()
app_server.stop()

if __name__ == "__main__":
    pytest.main()
