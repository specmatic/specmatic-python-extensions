import unittest

from specmatic.coverage.app_route_adapter import AppRouteAdapter
from specmatic.core.specmatic_mock import SpecmaticMock
from specmatic.core.specmatic_test import SpecmaticTest
from specmatic.generators.pytest_generator import PyTestGenerator
from specmatic.generators.unittest_generator import UnitTestGenerator
from specmatic.servers.app_server import AppServer
from specmatic.servers.asgi_app_server import ASGIAppServer
from specmatic.coverage.servers.coverage_server import CoverageServer
from specmatic.coverage.servers.fastapi_app_coverage_server import FastApiAppCoverageServer
from specmatic.coverage.servers.flask_app_coverage_server import FlaskAppCoverageServer
from specmatic.coverage.servers.sanic_app_coverage_server import SanicAppCoverageServer
from specmatic.servers.wsgi_app_server import WSGIAppServer
from specmatic.utils import get_junit_report_file_path


class Specmatic:
    def __init__(self):
        self.app = None
        self.app_module = ''
        self.app_host = '127.0.0.1'
        self.app_port = 0
        self.reset_app_config_func = None
        self.set_app_config_func = None
        self.app_server = None

        self.mock_host = None
        self.mock_port = None
        self.expectations = None
        self.mock_args = None
        self.mock = None

        self.test_class = None
        self.test_host = None
        self.test_port = None
        self.test_args = None

        self.project_root = ''
        self.specmatic_config_file_path = ''

        self.run_mock = False
        self.run_app = False
        self.run_tests = False

        self.coverage_server = None
        self.endpoints_api = ""

    def with_project_root(self, project_root):
        self.project_root = project_root
        return self

    def with_specmatic_config_file_path(self, specmatic_config_file_path):
        self.specmatic_config_file_path = specmatic_config_file_path
        return self

    def with_mock(self, mock_host: str = '127.0.0.1', mock_port: int = 0, expectations=None, args=None):
        self.mock_host = mock_host
        self.mock_port = mock_port
        self.run_mock = True
        self.expectations = expectations
        self.mock_args = args
        return self

    def app(self, app_server: AppServer):
        self.app_server = app_server
        self.run_app = True
        return self

    def with_wsgi_app(self, app, host: str = '127.0.0.1', port: int = 0, set_app_config_func=None,
                      reset_app_config_func=None):
        self.app = app
        self.app_host = host
        self.app_port = port
        self.set_app_config_func = set_app_config_func
        self.reset_app_config_func = reset_app_config_func
        self.run_app = True
        return self

    def with_asgi_app(self, app_module: str, host: str = '127.0.0.1', port: int = 0, set_app_config_func=None,
                      reset_app_config_func=None):
        self.app_module = app_module
        self.app_host = host
        self.app_port = port
        self.set_app_config_func = set_app_config_func
        self.reset_app_config_func = reset_app_config_func
        self.run_app = True
        return self

    def with_endpoints_api(self, endpoints_api):
        self.endpoints_api = endpoints_api
        return self

    def test(self, test_class, test_host: str = '127.0.0.1', test_port: int = 0, args=None):
        self.__setup_test_configuration(test_class, None, test_host, test_port, args)
        return self

    def test_with_api_coverage_for_flask_app(self, test_class, app, test_host: str = '127.0.0.1',
                                             test_port: int = 0, args=None):
        return self.__setup_test_configuration(test_class, FlaskAppCoverageServer(app), test_host, test_port, args)

    def test_with_api_coverage_for_sanic_app(self, test_class, app, test_host: str = '127.0.0.1',
                                             test_port: int = 0, args=None):
        return self.__setup_test_configuration(test_class, SanicAppCoverageServer(app), test_host, test_port, args)

    def test_with_api_coverage_for_fastapi_app(self, test_class, app, test_host: str = '127.0.0.1',
                                               test_port: int = 0, args=None):
        return self.__setup_test_configuration(test_class, FastApiAppCoverageServer(app), test_host, test_port, args)

    def test_with_api_coverage(self, test_class, app_route_adapter: AppRouteAdapter, test_host: str = '127.0.0.1',
                               test_port: int = 0, args=None):
        self.__setup_test_configuration(test_class, CoverageServer(app_route_adapter), test_host, test_port, args)
        return self

    def __setup_test_configuration(self, test_class, coverage_server: CoverageServer = None,
                                   test_host: str = '127.0.0.1',
                                   test_port: int = 0, args=None):
        self.test_class = test_class
        self.test_host = test_host
        self.test_port = test_port
        self.test_args = args
        self.run_tests = True
        self.coverage_server = coverage_server
        return self

    def __init_app_server(self):
        if self.run_app:
            if self.app is None and self.app_module == '':
                raise Exception('Please specify either an app or an app_module.')
            if self.app is not None and self.app_module != '':
                raise Exception('Please specify only one of app or app_module, and not both.')
            if self.app is not None:
                self.app_server = WSGIAppServer(self.app, self.app_host, self.app_port, self.set_app_config_func,
                                                self.reset_app_config_func)
            else:
                self.app_server = ASGIAppServer(self.app_module, self.app_host, self.app_port, self.set_app_config_func,
                                                self.reset_app_config_func)

    def __start_mock(self):
        if self.run_mock:
            self.mock = SpecmaticMock(self.mock_host, self.mock_port, self.project_root, self.specmatic_config_file_path,
                                      self.mock_args)
            self.mock.set_expectations(self.expectations)
            if self.app_server is not None:
                self.app_server.set_app_config(self.mock.host, self.mock.port)

    def __execute_tests(self):
        if self.run_tests:
            if self.app_server is not None:
                self.app_server.start()
                self.test_host = self.app_server.host
                self.test_port = self.app_server.port

            if self.endpoints_api == "":
                if self.coverage_server is not None:
                    self.coverage_server.start()
                    self.endpoints_api = self.coverage_server.endpoints_api

            SpecmaticTest(self.test_host, self.test_port, self.project_root,
                          self.specmatic_config_file_path, self.test_args, self.endpoints_api).run()

            if issubclass(self.test_class, unittest.TestCase):
                print("Injecting unittest methods")
                UnitTestGenerator(self.test_class, get_junit_report_file_path()).generate()
            else:
                print("Injecting pytest methods")
                PyTestGenerator(self.test_class, get_junit_report_file_path()).generate()

    def run(self):
        try:
            self.__init_app_server()
            self.__start_mock()
            self.__execute_tests()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            if self.coverage_server is not None:
                self.coverage_server.stop()
            if self.app_server is not None:
                self.app_server.stop()
                self.app_server.reset_app_config()
            if self.mock is not None:
                self.mock.stop()
