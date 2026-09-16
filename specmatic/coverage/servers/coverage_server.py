from flask import Flask, jsonify

from specmatic.coverage.app_route_adapter import AppRouteAdapter
from specmatic.servers.wsgi_app_server import WSGIAppServer


class CoverageServer:
    def __init__(self, app_route_adapter: AppRouteAdapter):
        self.app_route_adapter = app_route_adapter
        self.endpoints_api = ""
        self.app_server = None

    def start(self):
        print("\nStarting coverage server...")
        app = self.setup_coverage_flask_app()
        self.app_server = WSGIAppServer(app)
        self.app_server.start()
        coverage_server_url = f"http://{self.app_server.host}:{self.app_server.app_port}"
        print(f"\nCoverage server started on: {coverage_server_url}")
        self.endpoints_api = f"{coverage_server_url}/actuator/mappings"

    def stop(self):
        if self.app_server is None:
            return
        print("\nStopping coverage server...")
        self.app_server.stop()

    def setup_coverage_flask_app(self):
        app = Flask(__name__)
        routes = self.app_route_adapter.to_coverage_routes()

        @app.route('/actuator/mappings', methods=['GET'])
        def generate_actuator_mappings_endpoint_response():
            response = {
                "contexts": {
                    "application": {
                        "mappings": {
                            "dispatcherServlets": {
                                "dispatcherServlet": []
                            }
                        }
                    }
                }
            }

            for route in routes:
                response['contexts']['application']['mappings']['dispatcherServlets']['dispatcherServlet'].append({
                    "details": {
                        "requestMappingConditions": {
                            "methods": route.methods,
                            "patterns": [route.url]
                        }
                    }
                })
            print("\nResponse of /actuator/mappings route:")
            print(response)
            return jsonify(response)

        return app
