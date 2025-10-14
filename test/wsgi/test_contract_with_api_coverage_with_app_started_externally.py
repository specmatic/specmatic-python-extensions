import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.servers.wsgi_app_server import WSGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    ROOT_DIR,
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
)

app_server = WSGIAppServer(FLASK_APP, APP_HOST, APP_PORT)
app_server.start()


class TestContract:
    pass


Specmatic().with_project_root(ROOT_DIR).with_mock(
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
).test_with_api_coverage_for_flask_app(
    TestContract, FLASK_APP, APP_HOST, APP_PORT
).run()

app_server.stop()

if __name__ == "__main__":
    pytest.main()
