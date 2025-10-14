import socket
from time import sleep

import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.core.specmatic_mock import SpecmaticMock
from specmatic.utils import find_available_port
from test import RESOURCE_DIR, ROOT_DIR

app_host = "127.0.0.1"
app_port = 8000
stub_host = "127.0.0.1"
stub_port = 8080

invalid_expectation_json_file = ROOT_DIR + "/test/data/invalid_expectation.json"


class TestNegativeScenarios:
    def test_should_be_able_to_parse_randomly_assigned_stub_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 9000))
        try:
            stub = SpecmaticMock("127.0.0.1", project_root=ROOT_DIR)
            stub.stop()
        finally:
            sock.close()

    def test_should_use_passed_port_even_if_final_logs_contradict_it(self):
        stub = SpecmaticMock("127.0.0.1", 1234, project_root=ROOT_DIR)
        try:
            assert stub.port == 1234
        finally:
            stub.stop()

    def test_should_be_able_to_parse_port_when_base_url_has_postfix(self):
        multi_stub_conf = RESOURCE_DIR / "multi_base_url.yaml"
        stub = SpecmaticMock("127.0.0.1", specmatic_config_file_path=str(multi_stub_conf))
        try:
            stub.stop()
        finally:
            assert stub.port == "9002"

    def test_should_use_the_default_http_or_https_port_when_no_port_is_specified(self):
        port = SpecmaticMock._extract_port("- http://localhost/api")
        assert port == "80"

        port = SpecmaticMock._extract_port("- https://localhost/api")
        assert port == "443"

    def test_should_pick_first_port_when_multi_base_url_stub_is_used(self):
        multi_stub_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        stub = SpecmaticMock("127.0.0.1", specmatic_config_file_path=str(multi_stub_conf))
        try:
            stub.stop()
        finally:
            assert stub.port == "9000"

    def test_set_expectations_on_first_base_url_when_multi_port(self):
        multi_stub_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        example = f"{ROOT_DIR}/test/data/stub0.json"
        stub = SpecmaticMock("127.0.0.1", specmatic_config_file_path=str(multi_stub_conf))
        try:
            stub.set_expectations([example])
        finally:
            stub.stop()

    def test_expectations_should_fail_when_invalid_port_is_specified(self):
        multi_stub_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        example = f"{ROOT_DIR}/test/data/stub0.json"
        stub = SpecmaticMock("127.0.0.1", specmatic_config_file_path=str(multi_stub_conf))
        with pytest.raises(Exception):
            stub.set_expectations([example], 1234)
        stub.stop()

    def test_throws_exception_and_shuts_down_stub_when_stub_port_is_already_in_use(
        self,
    ):
        with pytest.raises(Exception) as exception:
            random_free_port = find_available_port()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("localhost", random_free_port))
            Specmatic().with_project_root(ROOT_DIR).with_mock(
                "127.0.0.1", random_free_port
            ).run()
            sock.close()
        assert (
            f"{exception.value}".find("Mock process terminated due to an error") != -1
        )

    def test_throws_exception_when_expectation_json_is_invalid(self):
        with pytest.raises(Exception) as exception:
            Specmatic().with_project_root(ROOT_DIR).with_mock(
                expectations=[invalid_expectation_json_file]
            ).with_asgi_app("test.apps.sanic_app:app").test(TestNegativeScenarios).run()
        assert f"{exception.value}".find("No match was found") != -1

    def test_throws_exception_when_app_module_is_invalid(self):
        with pytest.raises(Exception) as exception:
            Specmatic().with_asgi_app("main:app").with_project_root(ROOT_DIR).test(
                TestNegativeScenarios
            ).run()
        assert f"{exception.value}".find("App process terminated due to an error") != -1


if __name__ == "__main__":
    pytest.main()
