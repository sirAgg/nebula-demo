# nebula-demo

# 3.7.2 required for using FindVulkan
cmake_minimum_required(VERSION 3.7.2)

set( CMAKE_EXPORT_COMPILE_COMMANDS ON )

get_filename_component(FIPS_ROOT_DIR "../fips" ABSOLUTE)
include(${FIPS_ROOT_DIR}/cmake/fips.cmake)

project(lab1_project)
fips_setup(PROJECT nebula-demo)
fips_add_subdirectory(code)
fips_finish()
