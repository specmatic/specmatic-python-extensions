import pytest

from specmatic.core.specmatic import Specmatic
from test import (
    APP_HOST,
    APP_PORT,
    FLASK_APP,
    ROOT_DIR,
    STUB_HOST,
    STUB_PORT,
    expectation_json_files,
)


class TestContract:
    pass


Specmatic().with_project_root(ROOT_DIR).with_mock(
    STUB_HOST, STUB_PORT, expectation_json_files
).with_wsgi_app(
    FLASK_APP,
    APP_HOST,
    APP_PORT,
).test(TestContract).run()
if __name__ == "__main__":
    pytest.main()
