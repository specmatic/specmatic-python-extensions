import socket

import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.core.specmatic_mock import SpecmaticMock
from specmatic.utils import find_available_port
from test import RESOURCE_DIR, PROJECT_ROOT, PROJECT_ROOT_PATH

app_host = "127.0.0.1"
app_port = 8000
MOCK_HOST = "127.0.0.1"
MOCK_PORT = 8080

invalid_expectation_json_file = PROJECT_ROOT + "/test/data/invalid_expectation.json"


def block_v6(port: int):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    # Critical: ensure IPv6-only so this really occupies the IPv6 port
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    s.bind(("::", port))
    s.listen(1)
    return s


class TestNegativeScenarios:

    def test_should_be_able_to_parse_randomly_assigned_nock_port(self):
        sock6 = block_v6(9000)
        mock = None
        try:
            mock = SpecmaticMock(
                project_root=PROJECT_ROOT,
                specmatic_config_file_path=str(PROJECT_ROOT_PATH / "specmatic_config_without_ports.yaml")
            )
            assert mock.port is not None
            assert int(mock.port) != 9000
        finally:
            mock.stop()
            sock6.close()

    def test_should_use_passed_port_even_if_final_logs_contradict_it(self):
        mock = SpecmaticMock(
            host="127.0.0.1",
            port=1234,
            project_root=PROJECT_ROOT,
            specmatic_config_file_path=str(PROJECT_ROOT_PATH / "specmatic_config_without_ports.yaml")
        )
        try:
            assert mock.port == 1234
        finally:
            mock.stop()

    def test_should_be_able_to_parse_port_when_base_url_has_postfix(self):
        multi_mock_conf = RESOURCE_DIR / "multi_base_url.yaml"
        mock = SpecmaticMock(project_root=PROJECT_ROOT, specmatic_config_file_path=str(multi_mock_conf))
        try:
            mock.stop()
        finally:
            assert mock.port == "9002"

    def test_should_use_the_default_http_or_https_port_when_no_port_is_specified(self):
        host, port = SpecmaticMock._extract_host_port("- http://localhost/api")
        assert host == "localhost"
        assert port == "80"

        host, port = SpecmaticMock._extract_host_port("- https://localhost/api")
        assert host == "localhost"
        assert port == "443"

    def test_should_pick_first_port_when_multi_base_url_mock_is_used(self):
        multi_mock_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        mock = SpecmaticMock(project_root=PROJECT_ROOT, specmatic_config_file_path=str(multi_mock_conf))
        try:
            mock.stop()
        finally:
            assert mock.port == "9000"

    def test_set_expectations_on_first_base_url_when_multi_port(self):
        multi_mock_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        example = f"{PROJECT_ROOT}/test/data/stub0.json"
        mock = SpecmaticMock(project_root=PROJECT_ROOT, specmatic_config_file_path=str(multi_mock_conf))
        try:
            mock.set_expectations([example])
        finally:
            mock.stop()

    def test_expectations_should_fail_when_invalid_port_is_specified(self):
        multi_mock_conf = RESOURCE_DIR / "multi_base_url_with_default.yaml"
        example = f"{PROJECT_ROOT}/test/data/stub0.json"
        mock = SpecmaticMock(project_root=PROJECT_ROOT, specmatic_config_file_path=str(multi_mock_conf))
        with pytest.raises(Exception):
            mock.set_expectations([example], 1234)
        mock.stop()

    def test_throws_exception_and_shuts_down_mock_when_MOCK_PORT_is_already_in_use(
            self,
    ):
        with (pytest.raises(Exception) as exception):
            random_free_port = find_available_port()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pet_store_spec = str(RESOURCE_DIR / "pet_store.yaml")
            sock.bind(("localhost", random_free_port))
            (
                Specmatic()
                .with_mock("127.0.0.1", random_free_port, args=[pet_store_spec])
                .run()
            )
            sock.close()
        assert (
                f"{exception.value}".find("Mock process terminated due to an error") != -1
        )

    def test_throws_exception_when_expectation_json_is_invalid(self):
        with pytest.raises(Exception) as exception:
            (
                Specmatic(PROJECT_ROOT)
                .with_mock(expectations=[invalid_expectation_json_file])
                .with_asgi_app("test.apps.sanic_app:app")
                .test(TestNegativeScenarios)
                .run()
            )
        assert f"{exception.value}".find("No match was found") != -1

    def test_throws_exception_when_app_module_is_invalid(self):
        with pytest.raises(Exception) as exception:
            (
                Specmatic(PROJECT_ROOT)
                .with_asgi_app("main:app")
                .test(TestNegativeScenarios)
                .run()
            )
        assert f"{exception.value}".find("App process terminated due to an error") != -1


if __name__ == "__main__":
    pytest.main()
