cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(arba-hash CONFIG REQUIRED)

add_executable(example test_package.cpp)
target_link_libraries(example arba::hash)
# target_compile_features(${test_program} PRIVATE cxx_std_20)
