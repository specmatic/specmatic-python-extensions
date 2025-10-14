import unittest

from specmatic.core.specmatic_mock import SpecmaticMock
from specmatic.core.specmatic_test import SpecmaticTest
from specmatic.coverage.app_route_adapter import AppRouteAdapter
from specmatic.coverage.servers.coverage_server import CoverageServer
from specmatic.generators.pytest_generator import PyTestGenerator
from specmatic.generators.unittest_generator import UnitTestGenerator
from specmatic.servers.asgi_app_server import ASGIAppServer
from specmatic.servers.wsgi_app_server import WSGIAppServer
from specmatic.utils import get_junit_report_file_path


def specmatic_mock(host: str = '127.0.0.1', port: int = 0, project_root: str = '', expectations=None,
                   specmatic_config_file_path: str = ''):
    def decorator(cls):
        try:
            cls.mock = SpecmaticMock(host, port, project_root, specmatic_config_file_path)
            cls.mock.set_expectations(expectations)
        except Exception as e:
            if hasattr(cls, 'mock'):
                cls.mock.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e
        return cls

    return decorator


def specmatic_contract_test(host: str = '127.0.0,1', port: int = 0,
                                              project_root: str = '',
                                              specmatic_config_file_path: str = '', args=None, appRouteAdapter: AppRouteAdapter=None,):
    def decorator(cls):
        try:
            test_host = host
            test_port = port
            endpoints_api = ""
            if test_port == 0:
                if hasattr(cls, 'app'):
                    app = cls.app
                    test_host = app.host
                    test_port = app.port
            if appRouteAdapter:
                cls.coverage_server = CoverageServer(appRouteAdapter)
                cls.coverage_server.start()
                endpoints_api = cls.coverage_server.endpoints_api

            SpecmaticTest(test_host, test_port, project_root, specmatic_config_file_path, args,
                          endpoints_api).run()

            if issubclass(cls, unittest.TestCase):
                print("Injecting unittest methods")
                UnitTestGenerator(cls, get_junit_report_file_path()).generate()
            else:
                print("Injecting pytest methods")
                PyTestGenerator(cls, get_junit_report_file_path()).generate()
            return cls
        except Exception as e:
            if hasattr(cls, 'app'):
                cls.app.stop()
            if hasattr(cls, 'mock'):
                cls.mock.stop()
            if hasattr(cls, 'coverage_server'):
                cls.coverage_server.stop()
            print(f"Error: {e}")
            raise e
        finally:
            if hasattr(cls, 'mock'):
                cls.mock.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            if hasattr(cls, 'coverage_server'):
                cls.coverage_server.stop()

    return decorator


def start_wsgi_app(app, host: str = '127.0.0.1', port: int = 0):
    def decorator(cls):
        try:
            cls.app = WSGIAppServer(app, host, port)
            cls.app.start()
            return cls
        except Exception as e:
            if hasattr(cls, 'mock'):
                cls.mock.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e

    return decorator


def start_asgi_app(app_module: str, host: str = '127.0.0.1', port: int = 0):
    def decorator(cls):
        try:
            cls.app = ASGIAppServer(app_module, host, port)
            cls.app.start()
            return cls
        except Exception as e:
            if hasattr(cls, 'mock'):
                cls.mock.stop()
            if hasattr(cls, 'app'):
                cls.app.stop()
            print(f"Error: {e}")
            raise e

    return decorator
