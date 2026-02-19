import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    PROJECT_ROOT,
)


class TestContract:
    pass


(
    Specmatic(project_root=PROJECT_ROOT)
    .with_mock()
    .with_wsgi_app(FLASK_APP, APP_HOST, APP_PORT)
    .test_with_api_coverage_for_flask_app(TestContract, FLASK_APP)
    .run()
)

if __name__ == "__main__":
    pytest.main()
