cmake_minimum_required(VERSION 3.15)

project(PackageTest CXX)

find_package(arba-vrsn CONFIG REQUIRED)

set(test_program "test_package")

add_executable(${test_program}
    test_package.cpp
)
target_link_libraries(${test_program}
    PRIVATE
        arba::vrsn
)

target_compile_features(${test_program} PRIVATE cxx_std_20)
