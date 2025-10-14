import os
from pathlib import Path

from setuptools import setup, find_packages

from specmatic.build_utils import get_version, download_specmatic_jar

version = get_version(os.path.join('specmatic', 'version.py'))

download_specmatic_jar(version['__specmatic_version__'])

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='specmatic',
    python_requires='>=3.11',
    version=version['__version__'],
    description='A Python module for using the Specmatic Library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Specmatic Builders',
    author_email='info@core.in',
    url='https://github.com/specmatic/specmatic-python-extensions',
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    install_requires=[
        'pytest>=7.3.1',
        'requests>=2.26.0',
        'Werkzeug>=2.3.8',
        'uvicorn>=0.18.0',
        'fastapi>=0.70.0',
        'flask>=2.2.5',
        'sanic>=22.12.0'
    ]
)
