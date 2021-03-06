from conans import ConanFile, tools
from os import path


class ConanConfiguration(ConanFile):
    requires = [
        "exqudens-cpp-eval-conan-strings-lib/1.0.0"
    ]
    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [True, False]}
    generators = "cmake_paths", "cmake_find_package"

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="lib", src="lib")

    def set_name(self):
        self.name = path.basename(path.dirname(path.abspath(__file__)))

    def set_version(self):
        self.version = tools.load(path.join(path.dirname(path.dirname(path.abspath(__file__))), "version.txt")).strip()

    def package(self):
        self.copy("*")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)


if __name__ == "__main__":
    pass
