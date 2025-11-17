import json
import os
import subprocess
import threading
import traceback
from queue import Queue
from urllib.parse import urlparse

import requests

from specmatic.core.specmatic_base import SpecmaticBase


class SpecmaticMock(SpecmaticBase):

    def __init__(self, host: str = '127.0.0.1', port: int = 0, project_root: str = '',
                 specmatic_config_file_path: str = '', args=None):
        super().__init__(host, port, project_root, specmatic_config_file_path, args)
        self.__mock_started_event = None
        self.__process = None
        self.__free_port_message = 'Free port found'
        self.__mock_serving_message = 'serving endpoints from specs'
        self.__error_queue = Queue()
        self.__start()

    def __start(self):
        try:
            self.__mock_started_event = threading.Event()
            self.__start_specmatic_mock_in_subprocess()
            self.__start_reading_mock_output()
            self.__start_reading_mock_error_output()
            self.__wait_till_mock_has_started()
        except Exception as e:
            self.stop()
            print(f"Error: {e}")
            raise e

    def stop(self):
        if self.__process is not None:
            print(f"\n Shutting down specmatic mock server on {self.host}:{self.port}, please wait ...")
            self.__process.terminate()
            if self.__process.wait(5):
                print(f"\n Specmatic mock server on {self.host}:{self.port} has been shutdown successfully")
            else:
                print(f"\n Specmatic mock server on {self.host}:{self.port} did not shutdown in time, killing the process")
                self.__process.kill()

    def set_expectations(self, file_paths: list[str], port: int|None = None):
        port = port or self.port
        if port is None:
            raise Exception("The port needs to be specified, as the mock started on a random port and extraction failed from logs")

        if file_paths is None:
            file_paths = []

        try:
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    json_string = json.load(file)
                    headers = {
                        "Content-Type": "application/json"
                    }
                    response = requests.post(self.__get_expectations_api_url(port), json=json_string, headers=headers)
                    if response.status_code != 200:
                        self.stop()
                        raise Exception(f"{response.content} received for expectation json file: {json_string}")

        except Exception as e:
            self.stop()
            print(f"Error: {e}")
            raise e

    def __get_expectations_api_url(self, port):
        return f'http://{self.host}:{port}/_specmatic/expectations'

    def __start_specmatic_mock_in_subprocess(self):
        mock_command = self.__create_mock_process_command()
        if self.host != '' and self.port != 0:
            print(f"\n Starting specmatic mock server on {self.host}:{self.port}")
        self.__process = subprocess.Popen(mock_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def __start_reading_mock_output(self):
        stdout_reader = threading.Thread(target=self.__read_process_output, daemon=True)
        stdout_reader.start()

    def __start_reading_mock_error_output(self):
        error_reader = threading.Thread(target=self.__read_process_error_output, daemon=True)
        error_reader.start()

    def __wait_till_mock_has_started(self):
        self.__mock_started_event.wait()
        if not self.__error_queue.empty():
            error = self.__error_queue.get()
            raise Exception(f"An exception occurred while starting the mock: {error}")

    def __read_process_output(self):
        def signal_event_if_mock_has_started(line):
            if self.__free_port_message in line and self.port == 0:
                self.port = line.split(self.__free_port_message + ":")[1].strip()

            if self.__mock_serving_message in line:
                if self.port == 0:
                    self.port = self._extract_port(line.split(self.__mock_serving_message)[0])
                self.__mock_started_event.set()

        def read_and_print_output_line_by_line():
            for line in iter(self.__process.stdout.readline, ''):
                if line:
                    line = line.decode().rstrip()
                    print(line)
                    signal_event_if_mock_has_started(line)

        try:
            read_and_print_output_line_by_line()
        except Exception:
            tb = traceback.format_exc()
            self.__error_queue.put(tb)
            self.__mock_started_event.set()

    @staticmethod
    def _extract_port(text: str) -> str:
        for token in text.split():
            try:
                parsed = urlparse(token)
                if not parsed.hostname:
                    continue

                implicit_port = { "http": 80,"https": 443 }.get(parsed.scheme, None)
                port = parsed.port if parsed.port not in (None, -1) else implicit_port
                if port is not None:
                    return str(port)
            except ValueError:
                continue

        raise Exception(f"Unable to extract port from: {text}")

    def __read_process_error_output(self):
        try:
            for line in iter(self.__process.stderr.readline, ''):
                if line or self.__process.poll() is not None:
                    line = line.decode().rstrip()
                    print(line)
                    raise Exception('Mock process terminated due to an error ' + line)
        except Exception:
            tb = traceback.format_exc()
            self.__error_queue.put(tb)
            self.__mock_started_event.set()

    def __create_mock_process_command(self):
        return self.create_command_array('stub')
