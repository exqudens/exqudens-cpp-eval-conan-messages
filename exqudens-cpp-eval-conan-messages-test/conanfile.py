from conans import ConanFile, tools
from os import path


def get_version():
    return tools.load(path.join(path.dirname(path.dirname(path.abspath(__file__))), "version.txt")).strip()


class ConanConfiguration(ConanFile):
    requires = [
        "exqudens-cpp-eval-conan-messages-lib/" + get_version() + "@test-user/test-channel"
    ]
    settings = "arch", "os", "compiler", "build_type"

    def imports(self):
        self.copy(pattern="*", folder=True)