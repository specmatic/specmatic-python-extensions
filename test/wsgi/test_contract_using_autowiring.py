import pytest

from specmatic.core.specmatic import Specmatic
from test import FLASK_APP, PROJECT_ROOT, MOCK_HOST, MOCK_PORT, PROJECT_ROOT_PATH, RESOURCE_DIR


class TestContract:
    pass


def set_app_config(app, host: str, port: int):
    app.config["ORDER_API_HOST"] = host
    app.config["ORDER_API_PORT"] = str(port)
    app.config["API_URL"] = f"http://{host}:{port}"
    print(f"App config set to: {app.config['API_URL']}")


def reset_app_config(app):
    app.config["ORDER_API_HOST"] = MOCK_HOST
    app.config["ORDER_API_PORT"] = MOCK_PORT
    app.config["API_URL"] = f"http://{MOCK_HOST}:{MOCK_PORT}"


(
    Specmatic(PROJECT_ROOT)
    .with_specmatic_config_file_path(str(RESOURCE_DIR / "specmatic_config_without_ports.yaml"))
    .with_mock()
    .with_wsgi_app(FLASK_APP, set_app_config_func=set_app_config, reset_app_config_func=reset_app_config)
    .test_with_api_coverage_for_flask_app(TestContract, FLASK_APP)
    .run()
)

reset_app_config(FLASK_APP)

if __name__ == "__main__":
    pytest.main()
