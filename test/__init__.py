import pathlib

from test.apps.fast_api import app as FASTAPI_APP
from test.apps.flask_app import app as FLASK_APP
from test.apps.sanic_app import app as SANIC_APP
from test.utils import download_specmatic_jar_if_does_not_exist

download_specmatic_jar_if_does_not_exist()

ROOT_DIR = str(pathlib.Path.cwd().absolute())
RESOURCE_DIR = pathlib.Path.cwd() / "test" / "resources"

expectation_json_files = []
for file in pathlib.Path(ROOT_DIR, "test/data").iterdir():
    if (
        file.is_file()
        and file.suffix == ".json"
        and file.name != "invalid_expectation.json"
    ):
        expectation_json_files.append(file.absolute())  # noqa: PERF401


APP_HOST = "127.0.0.1"
APP_PORT = 5000
MOCK_HOST = "127.0.0.1"
MOCK_PORT = 8080

FASTAPI_APP = FASTAPI_APP
SANIC_APP = SANIC_APP
FLASK_APP = FLASK_APP

SANIC_STR = "test.apps.sanic_app:app"
FASTAPI_STR = "test.apps.fast_api:app"
