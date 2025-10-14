import pytest

from specmatic.core.specmatic import Specmatic
from test import FLASK_APP, ROOT_DIR, MOCK_HOST, MOCK_PORT, expectation_json_files


class TestContract:
    pass


def set_app_config(app, host: str, port: int):
    app.config["ORDER_API_HOST"] = host
    app.config["ORDER_API_PORT"] = str(port)
    app.config["API_URL"] = f"http://{host}:{port}"


def reset_app_config(app):
    app.config["ORDER_API_HOST"] = MOCK_HOST
    app.config["ORDER_API_PORT"] = MOCK_PORT
    app.config["API_URL"] = f"http://{MOCK_HOST}:{MOCK_PORT}"


Specmatic().with_project_root(ROOT_DIR).with_mock(
    expectations=expectation_json_files
).with_wsgi_app(
    FLASK_APP,
    set_app_config_func=set_app_config,
    reset_app_config_func=reset_app_config,
).test_with_api_coverage_for_flask_app(TestContract, FLASK_APP).run()

reset_app_config(FLASK_APP)

if __name__ == "__main__":
    pytest.main()
