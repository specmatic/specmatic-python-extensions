import os
import shutil
import subprocess

from specmatic.core.specmatic_base import SpecmaticBase
from specmatic.utils import get_junit_report_dir_path


class SpecmaticTest(SpecmaticBase):
    def __init__(self,
                 host: str | None = None,
                 port: int | None = None,
                 project_root: str | None = None,
                 specmatic_config_file_path: str | None = None,
                 args=None,
                 endpoints_api: str | None = None
                 ):
        super().__init__(host, port, project_root, specmatic_config_file_path, args, endpoints_api)

    def run(self):
        self._delete_existing_report_if_exists()
        self._execute_tests()

    def _delete_existing_report_if_exists(self):
        junit_report_dir_path = get_junit_report_dir_path()
        if os.path.exists(junit_report_dir_path):
            shutil.rmtree(junit_report_dir_path)

    def _execute_tests(self):
        cmd = self.create_command_array('test', get_junit_report_dir_path())
        print("command array:")
        print(cmd)
        print(f"\n Running specmatic tests for api at {self.host}:{self.port}")
        if self.project_root is not None:
            subprocess.run(cmd, cwd=self.project_root)
        else:
            subprocess.run(cmd)
