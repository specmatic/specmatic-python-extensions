import pytest

from specmatic.core.decorators import (
    specmatic_contract_test,
    specmatic_mock,
    start_wsgi_app,
)
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    PROJECT_ROOT,
    MOCK_HOST,
    MOCK_PORT,
    expectation_json_files,
)


# NOTE: Type Hint AppRouteAdapter in specmatic_contract_test decorator should be AppRouteAdapter | None
@specmatic_contract_test(project_root=PROJECT_ROOT)  # type: ignore[reportArgumentType]
@start_wsgi_app(FLASK_APP, APP_HOST, APP_PORT)
@specmatic_mock(project_root=PROJECT_ROOT)
class TestApiContract:
    pass


if __name__ == "__main__":
    pytest.main()
