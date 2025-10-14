from time import sleep

from specmatic.servers.app_server import AppServer
from specmatic.servers.wsgi_server_thread import WSGIServerThread
from specmatic.utils import find_available_port


class WSGIAppServer(AppServer):
    server: WSGIServerThread = None

    def __init__(self, app, host: str = '127.0.0.1', port: int = 0, set_app_config_func=None,
                 reset_app_config_func=None):
        self.app = app
        self.app_host = host
        self.app_port = find_available_port() if port == 0 else port
        self.set_app_config_func = set_app_config_func
        self.reset_app_config_func = reset_app_config_func
        self.daemon = True

    def start(self):
        self.server = WSGIServerThread(self.app, self.app_host, self.app_port)
        self.server.start()
        sleep(2)

    def stop(self):
        if self.server is not None:
            self.server.shutdown()

    @property
    def host(self):
        return self.app_host

    @property
    def port(self):
        return self.app_port

    def set_app_config(self, mock_host: str, mock_port: int):
        if self.set_app_config_func is not None:
            self.set_app_config_func(self.app, mock_host, mock_port)

    def reset_app_config(self):
        if self.reset_app_config_func is not None:
            self.reset_app_config_func(self.app)
