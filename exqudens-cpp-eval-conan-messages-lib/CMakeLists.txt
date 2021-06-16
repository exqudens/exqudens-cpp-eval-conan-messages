cmake_minimum_required(VERSION 3.20)
project("${CMAKE_PROJECT_NAME}-lib" VERSION "${CMAKE_PROJECT_VERSION}")

message("project: '${PROJECT_NAME}-${PROJECT_VERSION}'")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/bin")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE        "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL     "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG          "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE        "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL     "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG          "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE        "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL     "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG          "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")

set(CMAKE_MODULE_PATH "")
set(CMAKE_PREFIX_PATH "")
set(CONAN_INSTALL_PREFIX "${PROJECT_BINARY_DIR}/conan-install")
set("${PROJECT_NAME}_CMAKE_INSTALL_PREFIX" "${PROJECT_BINARY_DIR}/cmake-install")

if(DEFINED "CONAN_COMMAND")
    set(CONAN_PACKAGE_NAMES
        "exqudens-cpp-eval-conan-strings-lib"
    )

    set_conan_settings(CONAN_SETTINGS
        "${CMAKE_SYSTEM_NAME}"
        "${CMAKE_SYSTEM_PROCESSOR}"
        "${CMAKE_CXX_COMPILER_ID}"
        "${CMAKE_CXX_COMPILER_VERSION}"
        "${CMAKE_MSVC_RUNTIME_LIBRARY}"
        "${CMAKE_CXX_STANDARD}"
        "${CMAKE_BUILD_TYPE}"
    )

    set_conan_options(CONAN_OPTIONS
        "${BUILD_SHARED_LIBS}"
        "exqudens-cpp-eval-conan-strings-lib"
    )

    conan_install(
        "${CONAN_COMMAND}"
        "${PROJECT_SOURCE_DIR}/conanfile.py"
        "${CONAN_INSTALL_PREFIX}"
        "${CONAN_SETTINGS}"
        "${CONAN_OPTIONS}"
    )

    if(EXISTS "${CONAN_INSTALL_PREFIX}/conan_paths.cmake")
        set(CMAKE_MODULE_PATH "")
        set(CMAKE_PREFIX_PATH "")
        include("${CONAN_INSTALL_PREFIX}/conan_paths.cmake")
        set(CMAKE_MODULE_PATH "")
        set(CMAKE_PREFIX_PATH "")
        foreach(packageName ${CONAN_PACKAGE_NAMES})
            string(TOUPPER "${packageName}" packageNameUpper)
            if(DEFINED "CONAN_${packageNameUpper}_ROOT" AND IS_DIRECTORY "${CONAN_${packageNameUpper}_ROOT}")
                list(APPEND CMAKE_PREFIX_PATH "${CONAN_${packageNameUpper}_ROOT}")
            endif()
        endforeach()
    endif()

    add_custom_target_conan_export_user_channel("${PROJECT_NAME}-conan-export-testing"
        "${CONAN_COMMAND}"
        "${PROJECT_SOURCE_DIR}/conanfile.py"
        "test-user"
        "test-channel"
        "${${PROJECT_NAME}_CMAKE_INSTALL_PREFIX}"
        "${CONAN_SETTINGS}"
        "${CONAN_OPTIONS}"
    )

    add_custom_target_conan_export_user_channel_clean("${PROJECT_NAME}-conan-export-testing-clean"
        "${CONAN_COMMAND}"
        "${PROJECT_NAME}"
        "${PROJECT_VERSION}"
        "test-user"
        "test-channel"
    )

    add_custom_target_conan_export("${PROJECT_NAME}-conan-export"
        "${CONAN_COMMAND}"
        "${PROJECT_SOURCE_DIR}/conanfile.py"
        "${${PROJECT_NAME}_CMAKE_INSTALL_PREFIX}"
        "${CONAN_SETTINGS}"
        "${CONAN_OPTIONS}"
    )
endif()

find_package("exqudens-cpp-eval-conan-strings-lib" "1.0.0" QUIET CONFIG)

set_not_found_package_names(NOT_FOUND_PACKAGE_NAMES
    ${CONAN_PACKAGE_NAMES}
)

if(NOT "" STREQUAL "${NOT_FOUND_PACKAGE_NAMES}")
    foreach(package ${NOT_FOUND_PACKAGE_NAMES})
        message(WARNING "${package}_FOUND: '${${package}_FOUND}'")
    endforeach()
    return()
endif()

add_library("${PROJECT_NAME}"
    "src/main/cpp/exqudens/evaluation/Messages.hpp"
    "src/main/cpp/exqudens/evaluation/Messages.cpp"
)
target_include_directories("${PROJECT_NAME}" PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src/main/cpp>"
    "$<INSTALL_INTERFACE:include>"
)
set_property(TARGET "${PROJECT_NAME}" PROPERTY "VERSION" "${PROJECT_VERSION}")
set_property(TARGET "${PROJECT_NAME}" PROPERTY "SOVERSION" "${PROJECT_VERSION_MAJOR}")
set_property(TARGET "${PROJECT_NAME}" PROPERTY "INTERFACE_${PROJECT_NAME}_MAJOR_VERSION" "${PROJECT_VERSION_MAJOR}")
set_property(TARGET "${PROJECT_NAME}" APPEND PROPERTY "COMPATIBLE_INTERFACE_STRING" "${PROJECT_NAME}_MAJOR_VERSION")
target_link_libraries("${PROJECT_NAME}" PRIVATE
    "exqudens-cpp-eval-conan-strings-lib::exqudens-cpp-eval-conan-strings-lib"
)

install(
    TARGETS "${PROJECT_NAME}"
    EXPORT "${PROJECT_NAME}-targets"
    INCLUDES DESTINATION "include"
    RUNTIME DESTINATION "bin"
    LIBRARY DESTINATION "lib"
    ARCHIVE DESTINATION "lib"
)

install(
    DIRECTORY "src/main/cpp/"
    DESTINATION "include"
    FILES_MATCHING PATTERN "*.hpp"
)

install(
    EXPORT "${PROJECT_NAME}-targets"
    DESTINATION "cmake"
    NAMESPACE "${PROJECT_NAME}::"
    FILE "${PROJECT_NAME}-targets.cmake"
)

include(CMakePackageConfigHelpers)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake"
    INSTALL_DESTINATION "cmake"
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY "ExactVersion"
)

install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake"
          "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
    DESTINATION "cmake"
)

add_custom_target("${PROJECT_NAME}-cmake-install"
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_CURRENT_BINARY_DIR}" --prefix "${${PROJECT_NAME}_CMAKE_INSTALL_PREFIX}"
    COMMENT "execute: '${PROJECT_NAME}-cmake-install'"
    VERBATIM
)
