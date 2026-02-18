import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.servers.wsgi_app_server import WSGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    PROJECT_ROOT,
)

app_server = WSGIAppServer(FLASK_APP, APP_HOST, APP_PORT)
app_server.start()


class TestContract:
    pass


(
    Specmatic(PROJECT_ROOT)
    .with_mock()
    .test_with_api_coverage_for_flask_app(TestContract, FLASK_APP)
    .run()
)

app_server.stop()

if __name__ == "__main__":
    pytest.main()
