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
    ROOT_DIR,
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
)


# NOTE: Type Hint AppRouteAdapter in specmatic_contract_test decorator should be AppRouteAdapter | None
@specmatic_contract_test(APP_HOST, APP_PORT, ROOT_DIR)  # type: ignore[reportArgumentType]
@start_wsgi_app(FLASK_APP, APP_HOST, APP_PORT)
@specmatic_mock(STUB_HOST, STUB_PORT, ROOT_DIR, expectation_json_files)
class TestApiContract:
    pass


if __name__ == "__main__":
    pytest.main()
