import os


class SpecmaticBase:
    def __init__(self,
                 host: str | None = None,
                 port: int | None = None,
                 project_root: str | None = None,
                 specmatic_config_file_path: str | None = None,
                 args=None,
                 endpoints_api: str | None = None
                 ):
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

        if self.endpoints_api is not None:
            print("Setting Endpoints API as: " + self.endpoints_api)
            cmd.append("-DendpointsAPI=" + self.endpoints_api)

        cmd.append('-Dspecmatic.executor=python')
        cmd.append("-jar")
        cmd.append(jar_path)
        cmd.append(mode)

        if self.specmatic_config_file_path is not None:
            cmd.append("--config=" + self.specmatic_config_file_path)

        if self.host is not None:
            cmd += ['--host=' + self.host]
        if self.port is not None:
            cmd += ["--port=" + str(self.port)]
        if junit_dir_path != '':
            cmd += ["--junitReportDir=" + junit_dir_path]
        for arg in self.args:
            cmd += [arg]
        return cmd
