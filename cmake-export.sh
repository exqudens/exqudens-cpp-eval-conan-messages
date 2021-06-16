#!/bin/bash

cmake -S "." --preset "${1}" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-lib" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-test" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-lib-cmake-install" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-lib-conan-export-testing" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-package-test-conan-install" &&\
cmake -S "." --preset "${1}" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-package-test" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-lib-conan-export-testing-clean" &&\
cmake --build --preset "${1}" --target "exqudens-cpp-eval-conan-messages-lib-conan-export" &&\
echo 'BUILD_SUCCESSFUL' ||\
(echo 'BUILD_FAILED' && false)
