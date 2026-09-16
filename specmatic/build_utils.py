import http.client
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from specmatic.utils import get_project_root


GITHUB_RELEASE_URL = "https://github.com/specmatic/specmatic/releases/download/{version}/specmatic.jar"
REPOSILITE_RELEASE_URL = "https://repo.specmatic.io/releases/{artifact_path}"
MAVEN_RELEASE_URL = "https://repo1.maven.org/maven2/{artifact_path}"


def download_specmatic_jar(version):
    artifact_path = f"io/specmatic/specmatic-executable-all/{version}/specmatic-executable-all-{version}.jar"
    file_urls = [
        GITHUB_RELEASE_URL.format(version=version),
        REPOSILITE_RELEASE_URL.format(artifact_path=artifact_path),
        MAVEN_RELEASE_URL.format(artifact_path=artifact_path),
    ]
    file_path = Path(get_project_root()) / "specmatic/core/specmatic.jar"
    failures = []
    for file_url in file_urls:
        print(f"Downloading specmatic jar from: {file_url}")
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=file_path.parent, delete=False) as temporary_file:
                temporary_path = Path(temporary_file.name)
                with urllib.request.urlopen(file_url, timeout=60) as response:
                    shutil.copyfileobj(response, temporary_file)
            temporary_path.replace(file_path)
            print(f"Successfully downloaded Specmatic JAR from: {file_url}")
            return
        except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as error:
            failures.append(f"{file_url}: {error}")
            print(f"Download failed from {file_url}: {error}")
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
    raise RuntimeError(
        f"Unable to download Specmatic JAR version {version} from any source:\n"
        + "\n".join(failures)
    )


def get_version(version_py_path):
    version = {}
    with open(version_py_path) as file:
        exec(file.read(), version)
    return version
