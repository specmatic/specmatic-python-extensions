import os

import pytest
from specmatic.generators.pytest_generator import PyTestGenerator
from specmatic.generators.unittest_generator import UnitTestGenerator
from test import RESOURCE_DIR


class TestReportGeneration:
    junit_report_path = RESOURCE_DIR / "TEST-junit-jupiter.xml"

    def test_report_count_pytest(self):
        generator = PyTestGenerator(self, self.junit_report_path)
        generator.generate()

        pass_count, fail_count = 0, 0

        for func in self.__dict__.values():
            if "pass" in func.__name__:
                pass_count += 1
            elif "fail" in func.__name__:
                fail_count += 1

        assert pass_count + fail_count == 162
        assert pass_count == 159
        assert fail_count == 3

    def test_report_count_unittest(self):
        generator = UnitTestGenerator(self, self.junit_report_path)
        generator.generate()

        pass_count, fail_count = 0, 0

        for func in self.__dict__.values():
            if "pass" in func.__name__:
                pass_count += 1
            elif "fail" in func.__name__:
                fail_count += 1

        assert pass_count + fail_count == 162
        assert pass_count == 159
        assert fail_count == 3

    def test_report_generation_with_invalid_path(self):
        invalid_path = "path/to/invalid/junit/report"
        with pytest.raises(FileNotFoundError):
            PyTestGenerator(self, invalid_path).generate()

        with pytest.raises(FileNotFoundError):
            UnitTestGenerator(self, invalid_path).generate()
