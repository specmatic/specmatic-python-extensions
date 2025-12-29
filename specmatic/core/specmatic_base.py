import os


class SpecmaticBase:
    def __init__(self, host: str = '127.0.0.1', port: int = 0, project_root: str = '',
                 specmatic_config_file_path: str = '', args=None, endpoints_api=""):
        self.contract_file_paths = None
        self.project_root = project_root
        self.host = host
        self.port = port
        self.specmatic_config_file_path = specmatic_config_file_path
        self.args = [] if args is None else args
        self.endpoints_api = endpoints_api

    def create_command_array(self, mode: str, junit_dir_path=""):
        jar_path = os.path.dirname(os.path.realpath(__file__)) + "/specmatic.jar"
        cmd = ["java"]

        if self.endpoints_api != "":
            print("Setting Endpoints API as: " + self.endpoints_api)
            cmd.append("-DendpointsAPI=" + self.endpoints_api)

        cmd.append('-Dspecmatic.executor=python')
        cmd.append("-jar")
        cmd.append(jar_path)
        cmd.append(mode)

        if self.specmatic_config_file_path != '':
            cmd.append("--config=" + self.specmatic_config_file_path)

        cmd += ['--host=' + self.host]
        if self.port != 0:
            cmd += ["--port=" + str(self.port)]
        if junit_dir_path != '':
            cmd += ["--junitReportDir=" + junit_dir_path]
        for arg in self.args:
            cmd += [arg]
        return cmd
