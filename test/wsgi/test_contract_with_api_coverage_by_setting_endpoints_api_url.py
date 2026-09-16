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
