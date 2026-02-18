import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.coverage.servers.flask_app_coverage_server import FlaskAppCoverageServer
from specmatic.servers.wsgi_app_server import WSGIAppServer
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    PROJECT_ROOT,
)

app_server = WSGIAppServer(FLASK_APP, APP_HOST, APP_PORT)
coverage_server = FlaskAppCoverageServer(FLASK_APP)

app_server.start()
coverage_server.start()


class TestContract:
    pass


(
    Specmatic(PROJECT_ROOT)
    .with_mock()
    .with_endpoints_api(coverage_server.endpoints_api)
    .test(TestContract)
    .run()
)

app_server.stop()
coverage_server.stop()

if __name__ == "__main__":
    pytest.main()
